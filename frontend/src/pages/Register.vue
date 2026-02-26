<template>
  <div class="form-container">
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
      <center>
        <span class="text-success">{{ isFormValid ? 'Register Now' : 'Complete all fields' }} </span></center>
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
        <center><span class="text-primary">
          <RouterLink class="navbar-brand" style='text-align: center;' to="/login" >Already registered? Login</RouterLink>
        </span></center><br>
        <center><span class="text-secondary">
          <RouterLink class="navbar-brand" style='text-align: center;' to="/">Back</RouterLink></span></center>
      
      </div>
    </form>
  </div>
  
</template>

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

 <style>
/* body {
  background: linear-gradient(135deg, #1f2937 0%, #6f1c86 50%, #075bd1 100%);
  min-height: 100vh;
  padding: 2rem 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
} */

.form-container {
  max-width: 900px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 25px 60px rgba(0,0,0,0.25);
  border: 1px solid rgba(255,255,255,0.2);
}

.required {
  color: #ef4444;
  font-size: 0.85em;
  font-weight: bold;
}

.form-label {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.form-control, .form-select {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 0.875rem 1.25rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255,255,255,0.9);
  height: 56px;
}

.form-control:focus, .form-select:focus {
  border-color: #6f1c86;
  box-shadow: 0 0 0 0.25rem rgba(111,28,134,0.15);
  background: white;
  transform: translateY(-2px);
}

.btn-primary {
  background: linear-gradient(135deg, #1f2937 0%, #6f1c86 100%) !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 1rem 2rem !important;
  font-weight: 600 !important;
  font-size: 1.1rem !important;
  height: 56px !important;
  transition: all 0.3s ease !important;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(111,28,134,0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.invalid-feedback {
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

@media (max-width: 768px) {
  body { padding: 1rem 0; }
  .form-container {
    margin: 1rem;
    padding: 2rem 1.5rem;
  }
}
</style> 
