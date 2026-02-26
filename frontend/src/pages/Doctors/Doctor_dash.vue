<template>
<div>
    <div class ="top-section">
                <div id ="content" class="overflow-auto">
                        <h3 class="heading" >Upcoming Appointment</h3>
                        <div id="table1" class="border" style="max-height:150px;overflow-y: scroll;">
                        <table class="table table-striped table-bordered" >
                            <thead>
                                <tr>
                                    <th scope="col">Patient Name</th>
                                    <th scope="col">Date</th>
                                    <th scope="col">Time</th>
                                    <th scope="col">Treatment</th>
                                    <th scope="col">Action</th>
                                    
                                </tr>
                            </thead>
                            <div v-if="!appointments || appointments.length === 0" class="text-center p-3">
                                No upcoming appointments.
                            </div>
                            <tbody v-else>
                                <tr v-for="appointment in appointments" :key="appointment.id">
                                    <td>{{ appointment.patient_name }}</td>
                                    <td>{{ appointment.date }}</td>
                                    <td>{{ appointment.time }}</td>
                                    <td><RouterLink class="nav-link active" aria-current="page" :to="`/treatment/${appointment.id}`"><button class="btn btn-success">Update</button></RouterLink></td>
                                    <td><button class="btn btn-danger" @click="cancelAppointment(appointment.id)">Cancel</button></td>
                                </tr>
                            </tbody>
                        </table>
                        </div>
                </div>
            </div>
            <hr class="border border-primary border-3 opacity-75"> <!-- Boundary line which is dividing the 
            lower and upper part of the dashboard -->
     <div class ="bottom-section">
                <div id="content2" >
                    <h3 class="heading">Assigned Patients</h3>
                    <div id="table2" class="border" style="max-height: 270px;overflow-y: scroll;">
                    <table class="table table-striped table-bordered" >

                            <div v-if="!patients || patients.length === 0" class="text-center p-3">
                                No assigned patients.
                            </div>
                            <tbody v-else>
                            <tr v-for="patient in patients" :key="patient.id">
                                <th scope="col">{{ patient.name }}</th>
                                <RouterLink class="nav-link active" aria-current="page" :to="`/patient/history/${patient.id}`"><button class="btn btn-primary">View History</button></RouterLink>

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
// import { t } from 'vue-router/dist/index-DFCq6eJK';
export default {
    name: "Patient_dash",
    data() {
        return {
            token:"",
            user_type:"",
            appointments: [],
            patients: [],
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
            
            const response = axios.get("http://127.0.0.1:5000/api/doctor_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            response
            .then(res => {
                    this.patients = res.data.unique_patients;
                    this.appointments = res.data.appointments;
                    console.log(this.patients)
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
            this.patients = this.patients.filter(patient => patient.id !== res.data.patient_id);  // Remove patient from list
            // this.$router.push('/doctor_dash')
            this.loggingdashboard();
            })
            .catch(err => {
            console.error('Status:', err.response?.status);  // 401
            console.error('Error:', err.response?.data);     // {"message": "Invalid token"}
            });
        },
        loadPatients() {
      axios.get("http://127.0.0.1:5000/api/doctor_dashboard", {
        headers: {
          "Authentication-Token": this.token,
          "user_type": this.user_type
        }
      })
      .then(res => {
        this.patients = res.data.patients ;
      })
      .catch(err => console.error(err));
    },
    },
    // watch: {
    //     appointments(newVal) {
    //   this.loadPatients();
    // }
    // }
}




</script>