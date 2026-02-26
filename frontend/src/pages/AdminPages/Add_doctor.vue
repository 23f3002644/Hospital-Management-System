<template>
<div class="container mt-5">
            <div class="row">
                <div class="col-md-12">
                    
                    <h2 style="text-align: center;">Add New Doctor</h2>
                    <form @submit.prevent="addDoctor" class="mt-4">
                        
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" v-model="formData.email" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" v-model="formData.password" required>
                        </div>
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" v-model="formData.name" required>
                        </div>
                        <div class="mb-3">
                            <label for="age" class="form-label">Age</label>
                            <input type="number" class="form-control" id="age" v-model="formData.age" required>
                        </div>
                        <div class="mb-3">
                            <label for="address" class="form-label">Address</label>
                            <input type="text" class="form-control" id="address" v-model="formData.address" required>
                        </div>
                        <div class="mb-3">
                            <label for="contact_number" class="form-label">Contact Number</label>
                            <input type="number" class="form-control" id="contact_number" v-model="formData.contact_number" required>
                        </div>
                        <div class="mb-3">
                            <label for="gender" class="form-label">Gender</label>
                            <select class="form-select" id="gender" v-model="formData.gender" required>
                                <option value="" disabled selected>Select gender</option>   
                                <option value="male">Male</option>  
                                <option value="female">Female</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="specialty" class="form-label">Specialty</label>
                            <input type="text" class="form-control" id="specialty" v-model="formData.specialty" required>
                        </div>
                        <div class="mb-3">
                            <label for="department_name" class="form-label">Department Name</label>
                            <select class="form-select" id="department_name" v-model="formData.department_name" required>
                                <option value="" disabled selected>Select department</option>   
                                <option v-for="department in departments" :key="department.id" :value="department.name">{{ department.name }}</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea class="form-control" id="description" v-model="formData.description" rows="3" required></textarea>
                        </div>
                        
                        <div class="mb-3">
                            <button type="submit" class="btn btn-primary">Add Doctor</button>
                            <RouterLink to="/registered_doctors" class="btn btn-danger ms-2">Cancel</RouterLink>
                        </div>
                    </form>
                </div>
</div>
            </div>
</template>
<script>   
import axios from 'axios'; 
export default {
    data() {
        return {
            formData:{
                email: '',
                password: '',
                name: '',
                age: '',
                gender: '',
                specialty: '',
                department_name: '',
                description: '',
                address: '',
                contact_number: ''
            },
            token:"",
            user_type:"",
            departments: [],
            
        }
    },
    mounted(){
        this.tokenload()
        this.loadDepartment()
    },
    methods: {
        tokenload(){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
            const user_type = localStorage.getItem('user_type');
            if(user_type){
                this.user_type = user_type
            }
        },
        addDoctor(){
            // console.log("Adding Doctor")
            const response = axios.post(`http://127.0.0.1:5000/api/new_doctor`,JSON.stringify(this.formData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            response
            .then(res => {
                    // Handle the response data as needed
                    // console.log("2nd stage completed")
                    this.$router.push('/registered_doctors')
            }).catch(err => this.error = err.response.data.message)
        
        },
        loadDepartment(){
            const response = axios.get("http://127.0.0.1:5000/api/admin_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            response
            .then(res => {
                    // Handle the response data as needed
                    this.departments = res.data.departments;
            }).catch(err => this.error = err.response.data.message)
        
        }
    }
}
</script>