<template>
<div>
     <div class ="top-section">
                <div id="content2" >

                    <h3 class="heading">Departments</h3>

                    <div id="table2" class="border" style="max-height: 270px;overflow-y: scroll;">
                    <table class="table table-striped table-bordered" >
                        
                            <tr v-for="depart in departments" :key="depart.id">
                                <th scope="col">{{ depart.name }}</th>
                                <RouterLink :to="`/department_details/${depart.id}`"><button>View details</button></RouterLink>
                                
                            </tr>
                    </table>
                    </div>

                </div>
            </div>

            <hr class="border border-primary border-3 opacity-75"> <!-- Boundary line which is dividing the 
            lower and upper part of the dashboard -->
    <div class ="bottom-section">
                <div id ="content" class="overflow-auto">
                        <h3 class="heading" >Upcoming Appointment</h3>
                        <div id="table1" class="border" style="max-height:150px;overflow-y: scroll;">
                        <table class="table table-striped table-bordered" >
                            <thead>
                                <tr>
                                    <th scope="col">Doctor Name</th>
                                    <th scope="col">Department</th>
                                    <th scope="col">Appointment Date</th>
                                    <th scope="col">Appointment Time</th>
                                    <th scope="col">Action</th>
                                    
                                </tr>
                            </thead>
                            <div v-if="appointments.length === 0" class="text-center p-3">
                                No upcoming appointments.
                            </div>
                            <tbody v-else>
                                <tr v-for="appointment in appointments" :key="appointment.id">
                                    <td>{{ appointment.doctor_name }}</td>
                                    <td>{{ appointment.department_name }}</td>
                                    <td>{{ appointment.date }}</td>
                                    <td>{{ appointment.time }}</td>
                                    <td><button class="btn btn-danger" @click="cancelAppointment(appointment.id)">Cancel</button></td>
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
    name: "Patient_dash",
    data() {
        return {
            token:"",
            user_type:"",
            appointments: [],
            departments: [],
            appointmentId: null,
            // Data properties can be added here if needed
        };
    },
    mounted(){
            this.tokenload()
            this.loggingdashboard()

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
        loggingdashboard(){
            // event.preventDefault()
            // console.log(`Username: ${this.formData.username}, Password: ${this.formData.password}`)
            const response = axios.get("http://127.0.0.1:5000/api/patient_dashboard", {
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
                    this.appointments = res.data.appointments;
            }).catch(err => this.error = err.response.data.message)
        },
        cancelAppointment(appointmentId) {
            const response = axios.put(`http://127.0.0.1:5000/api/cancel_appointment/${appointmentId}`, {}, {
            headers: { "Authentication-Token": this.token }
            })
            response
            .then(res => {
            // console.log('Success:', res.data);
            this.appointments = this.appointments.filter(app => app.id !== appointmentId);
            })
            .catch(err => {
            console.error('Status:', err.response?.status);  // 401
            console.error('Error:', err.response?.data);     // {"message": "Invalid token"}
  });
        }
}
}




</script>