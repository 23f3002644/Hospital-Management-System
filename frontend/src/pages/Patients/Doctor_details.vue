<template>
    <div>
        <div class="container mt-5">
            <h2 class="mb-4">Doctor Details</h2>
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ doc_name }}</h5>
                    <div class="border p-3 mb-3">
                        <h6 class="card-subtitle mb-2 text-muted">Specialty: {{ doctors.specialty }}</h6>
                        <p class="card-text">Description: {{ doctors.description }}</p>
                        <h6 class="card-subtitle mb-2 text-muted">Gender: {{ doctors.gender }}</h6>
                        <h6 class="card-subtitle mb-2 text-muted">Address: {{ doctors.address }}</h6>
                        <h6 class="card-subtitle mb-2 text-muted">Contact: {{ doctors.contact_number }}</h6>
                        <h6 class="card-subtitle mb-2 text-muted">Age: {{ doctors.age }}</h6>
                        <h6 class="card-subtitle mb-2 text-muted">Department: {{ doctors.department_name }}</h6>
                    </div>
                </div>
            </div>
            <div>
                <RouterLink :to="`/department_details/${ this.dept_id }`"><button class="btn btn-primary mt-3">Back to Department</button></RouterLink>
                <RouterLink :to="`/appointment/${ doctors.department_name }/${ doctors.id }`"><button class="btn btn-primary mt-3">Book Appointment</button></RouterLink>
            </div>
        </div>

    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: "Doctor_details",
    data() {
        return {
            token:"",
            doctors: {},
            doc_name:"",
            dept_name:"",
            dept_id:null
            // Data properties can be added here if needed
        };
    },
    mounted(){
        this.tokenload()
        this.doctor_details()
        // console.log(this.doc_name)
        // console.log(this.dept_name)

    }
    ,
    methods:{
        tokenload(){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
        },
         doctor_details(){
            const doc_id = this.$route.params.id; // Assuming the route is defined with a parameter named 'name'
            // this.doc_name= doc_name
            const response = axios.get(`http://127.0.0.1:5000/api/doctor_details/${doc_id}`, {
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
                    this.doctors = res.data.doctor; // Assuming the API returns a single doctor object
                    this.dept_name = res.data.doctor.department_name; // Assuming the doctor object contains a department_name field
                    this.dept_id = res.data.dept_id; // Assuming the API returns the department ID
                    this.doc_name = res.data.doctor.name
                    console.log(this.dept_id);
            }).catch(err => this.error = err.response.data.message)


        }
    }
}

</script>