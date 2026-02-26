<template>
    <div>
        <!-- <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-12">
                    <h2 class="mb-4 text-center">Treatment History</h2>
                    <h5 >Name:    {{ this.name }}</h5>
                    <h5 >Gender:   {{ this.gender }}</h5>
                    <h5 >Age:     {{ this.age }}</h5>
                    <div class="card">
                        
                        <div class="card-body">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th scope="col">Doctor Name</th>
                                        <th scope="col">Department</th>
                                        <th scope="col">Treatment Date</th>
                                        <th scope="col">Appointment Time</th>
                                        <th scope="col">Diagnosis</th>
                                        <th scope="col">Prescription</th>
                                        <th scope="col">Test Done</th>
                                        <th scope="col">Medicine</th>
                                        <th scope="col">Visit Type</th>

                                    </tr>
                                </thead>
                                <div v-if="status_code === 404" class="text-center p-3">
                                    <h6>No Treatment history available.</h6>
                                </div>    
                                <tbody v-else>
                                    <tr v-for="appointment in appointments" :key="appointment.id">
                                        <td>{{ appointment.doctor_name }}</td>
                                        <td>{{ appointment.department_name }}</td>
                                        <td>{{ appointment.date }}</td>
                                        <td>{{ appointment.time }}</td>
                                        <td>{{ appointment.diagnosis }}</td>
                                        <td>{{ appointment.prescription }}</td>
                                        <td>{{ appointment.test_done }}</td>
                                        <td>{{ appointment.medicines }}</td>
                                        <td>{{ appointment.visit_type }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div> -->

        <div class ="bottom-section">
                <div id ="content" class="overflow-auto">
                        <h2 class="mb-4 text-center">Treatment History</h2>
                        <h5 >Name:    {{ this.name }}</h5>
                        <h5 >Gender:   {{ this.gender }}</h5>
                        <h5 >Age:     {{ this.age }}</h5>
                        <div id="table1" class="border" style="overflow-y: scroll;">
                        <table class="table table-striped table-bordered" >
                             <thead>
                                    <tr>
                                        <th scope="col">Doctor Name</th>
                                        <th scope="col">Department</th>
                                        <th scope="col">Treatment Date</th>
                                        <th scope="col">Appointment Time</th>
                                        <th scope="col">Diagnosis</th>
                                        <th scope="col">Prescription</th>
                                        <th scope="col">Test Done</th>
                                        <th scope="col">Medicine</th>
                                        <th scope="col">Visit Type</th>

                                    </tr>
                                </thead>
                            <div v-if="status_code === 404" class="text-center p-3">
                                    <h6>No Treatment history available.</h6>
                                </div>
                            <tbody v-else>
                                    <tr v-for="appointment in appointments" :key="appointment.id">
                                        <td>{{ appointment.doctor_name }}</td>
                                        <td>{{ appointment.department_name }}</td>
                                        <td>{{ appointment.date }}</td>
                                        <td>{{ appointment.time }}</td>
                                        <td>{{ appointment.diagnosis }}</td>
                                        <td>{{ appointment.prescription }}</td>
                                        <td>{{ appointment.test_done }}</td>
                                        <td>{{ appointment.medicines }}</td>
                                        <td>{{ appointment.visit_type }}</td>
                                    </tr>
                                </tbody>
                        </table>
                    </div>
                </div>
        </div>


    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: "History",
    data() {
        return {
            token:"",
            name:"",
            gender:"",
            age:"",
            appointments: [],
            id:"",
            status_code: null,
        };
    },
    mounted(){
            this.tokenload()
            
            const id = this.$route.params.id; 
            this.id = id; 
            this.fetchinghistory()
            // console.log(this.appointments)

    },
    methods: {
        tokenload(){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
            
        },
        fetchinghistory(){
            axios.get(`http://127.0.0.1:5000/api/patient_history/${this.id}`, {
                headers: {
                   "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                }       
            })
            .then(response => {
                this.gender = response.data.patient_gender;
                this.age = response.data.patient_age;
                this.status_code = response.data.status_code;
                this.name = response.data.patient_name;
                if (response.data.status_code === 404) {
                    this.appointments = null; // Set to null to indicate no appointments
                } else {
                    this.appointments = response.data.treatments; // Set to the treatments data
                }
                
            })
            .catch(error => {
                console.error('Error fetching dashboard data:', error);
            });
        }
    }
}
</script>