<template>
    <div>
        <h2 class="text-center">All Treatments</h2>

                    <div>
                    <h4 class="heading mt-2 text-center">Filter Here</h4>
                        <form class="d-flex mt-4" >
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model.trim="searchTerm" name="value">
                        <select class="form-select me-2" aria-label="Search by" v-model="searchKey" name="key">
                            <option value="patient">Patient Name</option>
                            <option value="doctor">Doctor Name</option>
                            <option value="department">Department</option>
                            <option value="date">Date</option>
                        </select>
                        </form>
                    </div>

        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-15">
                    <div class="table-responsive">
                        <table class="table table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>Patient Name</th>
                                    <th>Doctor Name</th>
                                    <th>Department</th>
                                    <th>Diagnosis</th>
                                    <th>Test done</th>
                                    <th>Prescription</th>
                                    <th>Medicines</th>
                                    <th>Visit date</th>
                                    <th>Time</th>
                                    <th>Visit Type</th>
                                    <th>Notes</th>
                                </tr>
                            </thead>
                            <tbody v-if="filteredTreatments.length === 0">
                                <tr>
                                    <td colspan="11" class="text-center">No treatments found.</td>
                                </tr>
                            </tbody>
                            <tbody v-else>
                                <tr v-for="treatment in filteredTreatments" :key="treatment.id">
                                    <td>{{ treatment.patient_name }}</td>
                                    <td>{{ treatment.doctor_name }}</td>
                                    <td>{{ treatment.department_name }}</td>
                                    <td>{{ treatment.diagnosis }}</td>
                                    <td>{{ treatment.test_done }}</td>
                                    <td>{{ treatment.prescription }}</td>
                                    <td>{{ treatment.medicines }}</td>
                                    <td>{{ treatment.date }}</td>
                                    <td>{{ treatment.time }}</td>
                                    <td>{{ treatment.visit_type }}</td>
                                    <td>{{ treatment.notes }}</td>                           
                                </tr> 
                            </tbody>
                        </table>
                    </div>
                </div>
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
            treatments: [],
            user_type: "",
            searchTerm: "",
            searchKey: "patient",
        };
    },
    mounted() {
        this.tokenload()
        this.treatmentLoad()
    },
    methods:{
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
        treatmentLoad(){
            
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
                    this.treatments = res.data.treatments;
            }).catch(err => this.error = err.response.data.message)
        },
    },
    computed: {
        filteredTreatments() {
            if (!this.searchTerm) {
                return this.treatments;
            }
            const term = this.searchTerm.toLowerCase();
            return this.treatments.filter(treatment => {
                if (this.searchKey === "patient") {
                    return treatment.patient_name.toLowerCase().includes(term);
                } else if (this.searchKey === "doctor") {
                    return treatment.doctor_name.toLowerCase().includes(term);
                } else if (this.searchKey === "department") {
                    return treatment.department_name.toLowerCase().includes(term);
                } else if (this.searchKey === "date") {
                    return treatment.date.toLowerCase().includes(term);
                }
                return false;
            });
        }
    }
}
</script>