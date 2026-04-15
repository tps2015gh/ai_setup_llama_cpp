package main

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"sync"
)

// User represents a user in the system
type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// UserStore manages users in memory
type UserStore struct {
	mu     sync.RWMutex
	users  []User
	nextID int
}

// NewUserStore creates a new user store
func NewUserStore() *UserStore {
	return &UserStore{
		users:  make([]User, 0),
		nextID: 1,
	}
}

// GetAll returns all users
func (s *UserStore) GetAll() []User {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.users
}

// GetByID returns a user by ID
func (s *UserStore) GetByID(id int) (*User, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	for _, u := range s.users {
		if u.ID == id {
			return &u, nil
		}
	}
	return nil, http.ErrMissingBoundary
}

// Create adds a new user
func (s *UserStore) Create(name, email string) *User {
	s.mu.Lock()
	defer s.mu.Unlock()

	user := User{
		ID:    s.nextID,
		Name:  name,
		Email: email,
	}
	s.nextID++
	s.users = append(s.users, user)
	return &user
}

// Delete removes a user by ID
func (s *UserStore) Delete(id int) bool {
	s.mu.Lock()
	defer s.mu.Unlock()

	for i, u := range s.users {
		if u.ID == id {
			s.users = append(s.users[:i], s.users[i+1:]...)
			return true
		}
	}
	return false
}

var store = NewUserStore()

func main() {
	http.HandleFunc("/users", usersHandler)
	http.HandleFunc("/users/", userByIDHandler)

	log.Println("Server starting on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// usersHandler handles /users endpoint
func usersHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		users := store.GetAll()
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"users": users,
			"count": len(users),
		})

	case http.MethodPost:
		var req struct {
			Name  string `json:"name"`
			Email string `json:"email"`
		}

		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Invalid request"})
			return
		}

		if req.Name == "" {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Name is required"})
			return
		}

		user := store.Create(req.Name, req.Email)
		writeJSON(w, http.StatusCreated, user)

	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "Method not allowed"})
	}
}

// userByIDHandler handles /users/{id} endpoint
func userByIDHandler(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Path[len("/users/"):]
	id, err := strconv.Atoi(idStr)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "Invalid ID"})
		return
	}

	switch r.Method {
	case http.MethodGet:
		user, err := store.GetByID(id)
		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "User not found"})
			return
		}
		writeJSON(w, http.StatusOK, user)

	case http.MethodDelete:
		if !store.Delete(id) {
			writeJSON(w, http.StatusNotFound, map[string]string{"error": "User not found"})
			return
		}
		writeJSON(w, http.StatusOK, map[string]string{"message": "User deleted"})

	default:
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "Method not allowed"})
	}
}

// writeJSON is a helper to write JSON responses
func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}
