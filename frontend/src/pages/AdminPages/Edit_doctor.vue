<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
        <div class="col-md-6">
            <h2 class="mb-4">Update Doctor Information</h2>
            <form @submit.prevent="updateDoctor">
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="new_form.name" :placeholder="old_form.name" required>
            </div>
            <div class="mb-3">
                <label for="age" class="form-label">Age</label>
                <input type="number" class="form-control" id="age" v-model="new_form.age" :placeholder="old_form.age" required>
            </div>
            <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <input type="text" class="form-control" id="address" v-model="new_form.address" :placeholder="old_form.address" required>
            </div>
            <div class="mb-3">
                <label for="contact_number" class="form-label">Contact Number</label>
                <input type="text" class="form-control" id="contact_number" v-model="new_form.contact_number" :placeholder="old_form.contact_number" required>
            </div>
            <div class="mb-3">
                            <label for="gender" class="form-label">Gender</label>
                            <select class="form-select" id="gender" v-model="new_form.gender" :placeholder="old_form.gender" required>
                                <option value="" disabled selected>Select gender</option>   
                                <option value="male">Male</option>  
                                <option value="female">Female</option>
                            </select>
                        </div>
            <div class="mb-3">
                <label for="specialty" class="form-label">Specialty</label>
                <input type="text" class="form-control" id="specialty" v-model="new_form.specialty" :placeholder="old_form.specialty" required>
            </div>
            <div class="mb-3">
                            <label for="department_name" class="form-label">Department Name</label>
                            <select class="form-select" id="department_name" v-model="new_form.department_name" :placeholder="old_form.department_name" required>
                                <option value="" disabled selected>Select department</option>   
                                <option v-for="department in departments" :key="department.id" :value="department.name">{{ department.name }}</option>
                            </select>
                        </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <input type="text" class="form-control" id="description" v-model="new_form.description" :placeholder="old_form.description" required>
            </div>
            <button type="submit" class="btn btn-success">Update</button>
            <RouterLink to="/registered_doctors" class="btn btn-danger ms-2">Cancel</RouterLink>
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
            token: "",
            departments: [],
            new_form:{
                name: '',
                age: '',
                address: '',
                contact_number: '',
                gender: '',
                specialty: '',
                department_name: '',
                description: ''

            },
            old_form:{
            }
        }
    },
    methods: {
        updateDoctor() {
            const doctorId = this.$route.params.id;
            const response = axios.put(`http://127.0.0.1:5000/api/update_doctor/${doctorId}`, JSON.stringify(this.new_form), {
            headers: { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Authentication-Token": this.token
             }
            })
            response
            .then(res => {
            // console.log('Success:', res.data);
            alert('Doctor information updated successfully!');
            this.$router.push('/registered_doctors');
            }).catch(err => this.error = err.response.data.message)
        },
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
        oldformload(){
            const doctorId = this.$route.params.id;
            
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
                    this.old_form = res.data.doctors.find(doctor => doctor.id == doctorId);
            }).catch(err => this.error = err.response.data.message)
        
        }
    },
    mounted() {
        this.tokenload();
        this.oldformload();
        }
    }

</script>