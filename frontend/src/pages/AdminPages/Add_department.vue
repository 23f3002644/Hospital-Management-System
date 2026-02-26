<template>
<div class="container mt-5">
            <div class="row">
                <div class="col-md-12">
                    
                    <h2 style="text-align: center;">Add New Department</h2>
                    <form @submit.prevent="addDepartment" class="mt-4">
                        
                        <div class="mb-3">
                            <label for="name" class="form-label">Department Name</label>
                            <input type="text" class="form-control" id="name" v-model="formData.name" required>
                        </div>
                        <div class="mb-3">
                            <label for="overview" class="form-label">Overview</label>
                            <textarea class="form-control" id="overview" v-model="formData.overview" rows="3" required></textarea>
                        </div>
                        <div class="mb-3">
                            <button type="submit" class="btn btn-primary">Add Department</button>
                            <RouterLink to="/all_departments" class="btn btn-danger ms-2">Cancel</RouterLink>
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
                name: '',
                overview: '',
            },
            token:"",
            user_type:"",
            departments: [],
            
        }
    },
    mounted(){
        this.tokenload()
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
        addDepartment(){
            console.log("Adding Department")
            const response = axios.post(`http://127.0.0.1:5000/api/new_department`,JSON.stringify(this.formData), {
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
                    console.log("2nd stage completed")
                    this.$router.push('/all_departments');
            }).catch(err => this.error = err.response.data.message)
        
        }
    }
}
</script>