<template>
  <div class="landing-container">
    <div class="content">
      
      <!-- Title and Description -->
      <h1 class="title">Welcome to Ayurveda Hospital</h1>
      <p class="description">
        Your trusted hospital management system for seamless patient care, 
        appointments, and medical records.
      </p>
      
      <!-- Action Buttons -->
      <div class="buttons">
        <RouterLink to="/login" class="btn btn-primary">
          <i class="bi bi-person"></i>Login
        </RouterLink>
        <RouterLink to="/register" class="btn btn-secondary">
          <i class="bi bi-plus-lg"></i>Register
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'


</script>

<style scoped>
.landing-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.content {
  text-align: center;
  max-width: 500px;
  color: white;
}


.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.description {
  font-size: 1.2rem;
  margin-bottom: 3rem;
  opacity: 0.95;
  line-height: 1.6;
}

.buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.btn-primary {
  background: #10b981;
  color: white;
}

.btn-primary:hover {
  background: #059669;
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(16,185,129,0.4);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(255,255,255,0.3);
}

.icon {
  font-size: 1.3rem;
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }
  
  .description {
    font-size: 1rem;
  }
  
  .buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 280px;
    justify-content: center;
  }
}
</style>