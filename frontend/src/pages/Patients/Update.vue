<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
        <div class="col-md-6">
            <h2 class="mb-4">Update Patient Information</h2>
            <form @submit.prevent="updatePatient">
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
            <button type="submit" class="btn btn-primary">Update</button>
            <RouterLink to="/patient_dash"><button class="btn btn-danger"> Back</button></RouterLink>
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
            new_form:{
                name: '',
                age: '',
                address: '',
                contact_number: ''
            },
            old_form:{
            }
        }
    },
    methods: {
        updatePatient() {
            const patientId = this.$route.params.id;
            const response = axios.put(`http://127.0.0.1:5000/api/update_patient/${patientId}`, JSON.stringify(this.new_form), {
            headers: { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Authentication-Token": this.token
             }
            })
            response
            .then(res => {
            const name = this.new_form.name
            localStorage.setItem("name", name)
            alert('Patient information updated successfully!');
            this.$router.push('/patient_dash');
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
            // event.preventDefault()
            // console.log(`Username: ${this.formData.username}, Password: ${this.formData.password}`)
            const response = axios.get("http://127.0.0.1:5000/api/patient_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                    
                }
            })
            response
            .then(res => {
                    // Handle the response data as needed
                    // this.departments = res.data.departments;
                    // this.appointments = res.data.appointments;
                    this.old_form = res.data.patient_details
            }).catch(err => this.error = err.response.data.message)
        }
    },
    mounted() {
        this.tokenload();
        this.oldformload();

        }
    }

</script>