<template>
    <div>
        <h3>Treatment Details </h3>
        <div class="card mb-3" style="max-width: 540px;">
            <div class="row g-0">
                <!-- <div class="col-md-4">
                    <img src="https://via.placeholder.com/150" class="img-fluid rounded-start" alt="Patient Image">
                </div> -->
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="card-text">Patient Name: {{ this.patient_name }}</h5>
                        <h5 class="card-text">Department: {{ this.Department_name }}</h5>
                    </div>
                </div>
            </div>
        </div>
        <form @submit.prevent="treatment">
            <div class="mb-3">
                <label for="diagnosis" class="form-label">Diagnosis</label>
                <input type="text" class="form-control" id="diagnosis" v-model="formData.diagnosis" required>
            </div>
            <div class="mb-3">
                <label for="test_done" class="form-label">Tests Done</label>
                <input type="text" class="form-control" id="test_done" v-model="formData.test_done" required>
            </div>
            <div class="mb-3">
                <label for="prescription" class="form-label">Prescription</label>
                <input type="text" class="form-control" id="prescription" v-model="formData.prescription" required>
            </div>
            <div class="mb-3">
                <label for="medicines" class="form-label">Medicines</label>
                <input type="text" class="form-control" id="medicines" v-model="formData.medicines" required>
            </div>
            <div class="mb-3">
                <label for="visit_type" class="form-label">Visit Type</label>
                <select class="form-select" id="visit_type" v-model="formData.visit_type" required>
                    <option value="">Select Visit Type</option>
                    <option value="first_time">First Time</option>
                    <option value="follow_up">Follow Up</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="notes" class="form-label">Additional Notes</label>
                <textarea class="form-control" id="notes" rows="3" v-model="formData.notes" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit Treatment Details</button>
            <RouterLink to="/doctor_dash"><button class="btn btn-danger"> Back</button></RouterLink>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "Treatment",
    data() {
        return {
            token:"",
            user_type:"",
            formData:{
                diagnosis: "",
                test_done: "",
                prescription: "",
                medicines: "",
                visit_type: "",
                notes: ""
            },
            patient_name: "",
            Department_name: "",
            appointment_id:"",
    
            // Data properties can be added here if needed
        };
    },
    mounted(){
        this.tokenload()
        this.appointment_id = this.$route.params.id;
        this.loggingdashboard()
        // Code to fetch treatment details can be added here
    },
    methods: {
        tokenload(){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
            // console.log(this.token)
            const user_type = localStorage.getItem('user_type');
            if(user_type){
                this.user_type = user_type
            }
        },
        treatment(){
            const id = this.$route.params.id;
            console.log("1st stage completed")
            const response = axios.post(`http://127.0.0.1:5000/api/treatment/${id}`,JSON.stringify(this.formData), {
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
                    this.$router.push('/doctor_dash')
            }).catch(err => this.error = err.response.data.message)
        },
        loggingdashboard(){
            // event.preventDefault()
            // console.log(`Username: ${this.formData.username}, Password: ${this.formData.password}`)
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
                    // Handle the response data as needed
                    const appointments = res.data.appointments;
                    // console.log(appointments)
                    for (let appointment of appointments) {
                        // console.log(appointment.id, this.$route.params.id)
                        if (appointment.id == this.appointment_id) {
                            this.patient_name = appointment.patient_name;
                            // console.log(appointment.patient_name)
                            this.Department_name = appointment.department_name;
                            // console.log(appointment.department_name)
                            break;
                        }
                    }
                    // console.log(this.patient_name)
                    // console.log(this.Department_name)
                    
                    // this.appointments = res.data.appointments;
            }).catch(err => this.error = err.response.data.message)
        }
        // Methods to handle treatment updates can be added here
    }
}
</script>