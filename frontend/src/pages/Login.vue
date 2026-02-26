<script>
import axios from 'axios'
export default {
    data(){
        return {
           formData:{
            email: "",
            password: ""
           },
           token: "",
           user_type:"",
           name:'',
           error: "" 
        }
    },
    methods:{
        loginUser(){
            // event.preventDefault()
            // console.log(`Username: ${this.formData.username}, Password: ${this.formData.password}`)
            const response = axios.post("http://127.0.0.1:5000/api/login", JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            })
            response
            .then(res => {
                    this.token = res.data.token
                    localStorage.setItem("token", res.data.token)
                    this.user_type = res.data.user_type
                    localStorage.setItem("user_type", res.data.user_type)
                    this.name = res.data.name
                    localStorage.setItem("name",res.data.name)
                    localStorage.setItem("id", res.data.id)
                    if (this.user_type=="admin"){
                      this.$router.push('/dashboard')
                    }else if (this.user_type=="doctor"){
                      this.$router.push('/doctor_dash')
                    } else {
                      this.$router.push('/patient_dash')
                    }
                    
            }).catch(err => this.error = err.response.data.message)


            // alternative
            // catch((err) => {
            //     this.error = err.response.data.message
            // })
        }
    }
}
</script>

<template>
    <div id="hello">
        <div id="canvas">
            <div id="form-body">
                <h1>Login Form</h1>
                
                <form @submit.prevent="loginUser">
                <div class="mb-3">
                    <label for="Input1" class="form-label">Email</label>
                    <input type="email" class="form-control" id="Input1" v-model="formData.email">
                </div>
                <div class="mb-3">
                    <label for="Input2" class="form-label">Password</label>
                    <input type="password" class="form-control" id="Input2" v-model="formData.password" >
                </div>
                <p class="err" v-if="error">{{ error }}</p>
                <div style="text-align: center;">
                <input type="submit" class="btn btn-primary" value="Login"> <br>
                <!-- <button @click="" class="btn btn-primary">Login</button> <br> -->
                <RouterLink class="navbar-brand" to="/register">Don't have an account? Register</RouterLink><br>
                <RouterLink class="navbar-brand" to="/">Back</RouterLink>
               </div>
               </form>
               
               <!-- <button @click="logoutUser" class="btn btn-danger">Logout</button> -->
            </div>
        </div>
    </div>
</template>


<style>
#hello {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1f2937 0%, #6f1c86 50%, #075bd1 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

#canvas {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 3rem 2.5rem;
  box-shadow: 0 25px 50px rgba(0,0,0,0.25);
  width: 100%;
  max-width: 420px;
  border: 1px solid rgba(255,255,255,0.2);
}

#form-body {
  height: auto; /* Fixed: was 337px */
}

h1 {
  text-align: center;
  color: #1f2937;
  margin-bottom: 2rem;
  font-weight: 700;
  font-size: 2.2rem;
  background: linear-gradient(135deg, #1f2937 0%, #6f1c86 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.form-control {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255,255,255,0.9);
  height: 56px;
}

.form-control:focus {
  border-color: #6f1c86;
  box-shadow: 0 0 0 0.25rem rgba(111,28,134,0.15);
  background: white;
  transform: translateY(-2px);
  outline: none;
}

.mb-3 {
  margin-bottom: 1.5rem !important;
}

input[type="submit"].btn-primary {
  background: linear-gradient(135deg, #1f2937 0%, #6f1c86 100%) !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 1rem 2.5rem !important;
  font-weight: 600 !important;
  font-size: 1.1rem !important;
  width: 100% !important;
  height: 56px !important;
  transition: all 0.3s ease !important;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 10px 30px rgba(111,28,134,0.3);
}

input[type="submit"].btn-primary:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 15px 40px rgba(111,28,134,0.4) !important;
}

input[type="submit"].btn-primary:active {
  transform: translateY(-1px) !important;
}

div[style="text-align: center;"] {
  margin-top: 1.5rem !important;
}

div[style="text-align: center;"] a {
  color: #6f1c86;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

div[style="text-align: center;"] a:hover {
  color: #1f2937;
  text-decoration: underline;
}

.err {
  color: #ef4444;
  background: rgba(239,68,68,0.1);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border-left: 4px solid #ef4444;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 576px) {
  #canvas {
    margin: 1rem;
    padding: 2rem 1.5rem;
  }
  h1 {
    font-size: 1.8rem;
  }
}
</style>