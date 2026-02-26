<template>
<div class="container mt-5">
            <div class="row">
                <div class="col-md-12">
                    <h2>Upcoming Appointments</h2>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Patient Name</th>
                                    <th scope="col">Doctor Name</th>
                                    <th scope="col">Department</th>
                                    <th scope="col">Date</th>
                                    <th scope="col">Time</th>
                                    <th scope="col">Patient History</th>
                                </tr>
                            </thead>
                            <tbody v-if="appointments.length === 0">
                                <tr>
                                    <td colspan="5" class="text-center">No appointments found.</td>
                                </tr>
                            </tbody>
                            <tbody v-else>
                                <tr v-for="appointment in appointments" :key="appointment.id" >
                                    
                                    <td v-if="appointment.status==='booked'">{{ appointment.patient_name }}</td>
                                    <td v-if="appointment.status==='booked'">{{ appointment.doctor_name }}</td>
                                    <td v-if="appointment.status==='booked'">{{ appointment.department_name }}</td>
                                    <td v-if="appointment.status==='booked'">{{ appointment.date }}</td>
                                    <td v-if="appointment.status==='booked'">{{ appointment.time }}</td>
                                    <td v-if="appointment.status==='booked'"><RouterLink class="nav-link active" aria-current="page" :to="`/patient/history/${appointment.patient_id}`"><button class="btn btn-primary">View History</button></RouterLink></td>
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
    name: "Upcoming_Appointments",
    data() {
        return {
            token:"",
            user_type:"",
            appointments: [],
        };
    },
    mounted(){
            this.tokenload()
            this.upcomingAppointment()

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
        upcomingAppointment(){
            // event.preventDefault()
            // console.log(`Username: ${this.formData.username}, Password: ${this.formData.password}`)
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
                    this.appointments = res.data.appointments;
            }).catch(err => this.error = err.response.data.message)
        }
        
    }
}
</script>