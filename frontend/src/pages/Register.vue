<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
        name: '',
        contact_number: '',
        age: null,
        gender: '',
        address: ''
      },
      errors: {},
      error:""
    }
  },
  computed: {
    isFormValid() {
      return this.form.email &&
           this.form.password.length >= 6 &&
           this.form.name &&
           this.form.age &&
           this.form.contact_number.length === 10 &&
           this.form.gender &&
           this.form.address;
    }
  },
  methods: {
    handleSubmit() {
      const response = axios.post("http://127.0.0.1:5000/api/register", this.form,{
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
      })
      response
      .then(res => {
        this.$router.push('/login')
        alert('Registration Successful, you can login now')
        
      }).catch(err => this.error = err.response.data.message )
    }
  }
}
</script>

<template>
  <div class="form-container">
    <div class="form-card">
      <h1>Register Form</h1>
      <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ error }}  <!-- Shows "User already exists" -->
        
      </div>
      <form class="row g-3" @submit.prevent="handleSubmit">
        <div class="col-md-6">
          <label for="inputEmail4" class="form-label">Email <span class="required">*</span></label>
          <input type="email" class="form-control" id="inputEmail4" v-model="form.email":class="{ 'is-invalid': errors.email }"
          placeholder="abc@gmail.com" required>
          <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
        </div>
        
        <div class="col-md-6">
          <label for="inputPassword4" class="form-label">Password <span class="required">*</span></label>
          <input type="password" class="form-control" id="inputPassword4"v-model="form.password":class="{ 'is-invalid': errors.password }"
          required>
          <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
        </div>
        
        <div class="col-md-6">
          <label for="inputName" class="form-label">Name <span class="required">*</span></label>
          <input type="text" class="form-control" id="inputName"v-model="form.name":class="{ 'is-invalid': errors.name }"
          required>
          <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
        </div>
        
        <div class="col-md-6">
          <label for="inputPhone" class="form-label">Contact Number <span class="required">*</span></label>
          <input type="tel" class="form-control" id="inputPhone" v-model="form.contact_number" :class="{ 'is-invalid': errors.phone }"
          required>
          <div v-if="errors.phone" class="invalid-feedback">{{ errors.phone }}</div>
        </div>
        
        <div class="col-md-6">
          <label for="inputAge" class="form-label">Age <span class="required">*</span></label>
          <input type="number" class="form-control" id="inputAge" v-model.number="form.age" :class="{ 'is-invalid': errors.age }"
            min="18" max="100"
            required>
          <div v-if="errors.age" class="invalid-feedback">{{ errors.age }}</div>
        </div>
        
        <div class="col-md-6">
          <label for="inputGender" class="form-label">Gender <span class="required">*</span></label>
          <select class="form-control" id="inputGender" v-model="form.gender" :class="{ 'is-invalid': errors.gender }" required>
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
          <div v-if="errors.gender" class="invalid-feedback">{{ errors.gender }}</div>
        </div>
        
        <div class="col-12">
          <label for="inputAddress" class="form-label">Address <span class="required">*</span></label>
          <input type="text" class="form-control" id="inputAddress" v-model="form.address" :class="{ 'is-invalid': errors.address }"
            placeholder="Enter your full address" required>
          <div v-if="errors.address" class="invalid-feedback">{{ errors.address }}</div>
        </div>
        <div class="center-text">
          <span class="text-success">{{ isFormValid ? 'Register Now' : 'Complete all fields' }} </span></div>
        <div class="col-12">
          <input
            type="submit" 
            class="btn btn-primary w-100" 
            :disabled="!isFormValid"
          >
          <div>
            <br>
          </div>
          <!-- </button>
          <input type="submit" class="btn btn-primary" value="Login"> <br> -->
          <div class="center-text"><span class="text-primary">
            <RouterLink class="navbar-brand" style='text-align: center;' to="/login" >Already registered? Login</RouterLink>
          </span></div><br>
          <div class="heading"><span class="text-secondary ">
            <RouterLink class="navbar-brand" style='text-align: center;' to="/">Back</RouterLink></span></div>
          
        </div>
      </form>
    </div>
  </div>
</template>

<style>
.form-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 30%, #a78bfa 60%, #8b5cf6 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  position: relative;
  overflow: hidden;
}

.form-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(168,85,247,0.25) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(139,92,246,0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(147,51,234,0.15) 0%, transparent 50%);
  pointer-events: none;
  z-index: 1;
  animation: pulseGlow 4s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
}

.form-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border-radius: 24px;
  padding: 3.5rem 3rem;
  box-shadow: 
    0 35px 70px rgba(0,0,0,0.15),
    0 0 0 1px rgba(255,255,255,0.8),
    inset 0 1px 0 rgba(255,255,255,0.6),
    0 8px 30px rgba(139,92,246,0.1);
  width: 100%;
  max-width: 950px;
  border: 2px solid rgba(139,92,246,0.3);
  position: relative;
  z-index: 2;
  animation: slideUpFloat 0.8s cubic-bezier(0.4, 0, 0.2, 1) both;
}

/* .form-card::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #8b5cf6, #a78bfa, #c084fc, #8b5cf6);
  border-radius: 26px;
  z-index: -1;
  padding: 2px;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  animation: borderRotate 3s linear infinite;
} */

/* @keyframes borderRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
} */

@keyframes slideUpFloat {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.form-card > h1 {
  position: relative;
  z-index: 3;
  text-align: center;
  color: #581c87;
  margin-bottom: 2.5rem;
  font-weight: 800;
  font-size: clamp(1.75rem, 4vw, 2.6rem);
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #c084fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.025em;
}

.form-card > h1::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  border-radius: 2px;
  box-shadow: 0 2px 10px rgba(139,92,246,0.5);
}

.form-card > .alert {
  position: relative;
  z-index: 3;
  background: linear-gradient(135deg, rgba(239,68,68,0.2) 0%, rgba(220,38,38,0.15) 100%);
  backdrop-filter: blur(15px);
  border: 2px solid rgba(239,68,68,0.4);
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 8px 25px rgba(239,68,68,0.25);
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.row.g-3 {
  position: relative;
  z-index: 3;
}

.required {
  color: #ef4444;
  font-size: 0.85em;
  font-weight: bold;
  animation: pulseDot 2s ease-in-out infinite;
}

@keyframes pulseDot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.form-label {
  font-weight: 600;
  color: #581c87;
  margin-bottom: 1rem;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-label::before {
  content: '✨';
  font-size: 1.1rem;
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from { opacity: 0.6; transform: scale(1); }
  to { opacity: 1; transform: scale(1.1); }
}

.form-control, .form-select {
  border: 2px solid rgba(139,92,246,0.2);
  border-radius: 20px;
  padding: 1.25rem 1.75rem;
  font-size: 1rem;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255,255,255,0.97);
  height: 65px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.form-control:focus, .form-select:focus {
  border-color: #8b5cf6;
  box-shadow: 
    0 0 0 0.4rem rgba(139,92,246,0.2),
    0 12px 35px rgba(139,92,246,0.25),
    inset 0 1px 0 rgba(255,255,255,0.9);
  background: rgba(255,255,255,1);
  transform: translateY(-3px);
  outline: none;
}

.form-control::placeholder {
  color: #c4b5fd;
  font-weight: 500;
}

.is-invalid {
  border-color: #ef4444 !important;
  box-shadow: 0 0 0 0.3rem rgba(239,68,68,0.25) !important;
  animation: shakeField 0.5s ease-in-out;
}

@keyframes shakeField {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  75% { transform: translateX(2px); }
}

.invalid-feedback {
  color: #dc2626;
  font-weight: 600;
  font-size: 0.9rem;
  margin-top: 0.75rem;
}

.btn-primary {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 50%, #5b21b6 100%) !important;
  border: 2px solid rgba(124,58,237,0.3) !important;
  border-radius: 20px !important;
  padding: 1.375rem 3.5rem !important;
  font-weight: 700 !important;
  font-size: 1.2rem !important;
  height: 70px !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  text-transform: uppercase;
  letter-spacing: 1.25px;
  box-shadow: 
    0 15px 40px rgba(124,58,237,0.45),
    0 6px 20px rgba(0,0,0,0.15),
    inset 0 1px 0 rgba(255,255,255,0.35);
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.8s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-5px) scale(1.03) !important;
  box-shadow: 
    0 25px 50px rgba(124,58,237,0.55),
    0 0 0 2px rgba(124,58,237,0.4),
    inset 0 1px 0 rgba(255,255,255,0.5) !important;
}

.btn-primary:hover:not(:disabled)::before {
  left: 100%;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  background: linear-gradient(135deg, #9ca3af, #6b7280) !important;
  border-color: rgba(156,163,175,0.5) !important;
}

.text-success {
  color: #10b981 !important;
  font-weight: 700;
  font-size: 1.2rem;
  text-shadow: 0 2px 4px rgba(16,185,129,0.3);
}

RouterLink.navbar-brand {
  color: #8b5cf6;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
  display: inline-block;
  padding: 1rem 0;
}

RouterLink.navbar-brand::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 3px;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
  border-radius: 2px;
  transition: width 0.4s ease;
}

RouterLink.navbar-brand:hover {
  color: #6d28d9;
  transform: translateY(-2px);
}

RouterLink.navbar-brand:hover::after {
  width: 100%;
}

center {
  position: relative;
  z-index: 3;
}

@media (max-width: 768px) {
  .form-card {
    margin: 1rem;
    padding: 2.5rem 2rem;
    border-radius: 20px;
  }
  
  .form-card > h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  .form-control, .form-select {
    height: 60px;
    padding: 1.125rem 1.5rem;
  }
  
  .btn-primary {
    height: 65px !important;
    padding: 1.25rem 3rem !important;
    font-size: 1.1rem !important;
  }
}

@media (max-width: 480px) {
  .form-card {
    padding: 2rem 1.5rem;
  }
  
  .form-card > h1 {
    font-size: 1.8rem;
  }
}
</style>
