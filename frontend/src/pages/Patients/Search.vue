<template>
    <div>
        <div>
        <h4 class="heading mt-2 text-center">Filter Here</h4>
        <form class="d-flex mt-4" >
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model.trim="searchTerm" name="value">
                <select class="form-select me-2" aria-label="Search by" v-model="searchKey" name="key">
                    <option value="doctor">Doctor name</option>
                    <option value="department">Department</option>
                </select>
            
        </form>
        </div>

        <div class ="bottom-section">
                <div id ="content" class="overflow-auto">
                        <h3 class="heading mt-2 text-center" >Doctor's List</h3>
                        <div id="table1" class="border" style="overflow-y: scroll;">
                        <table class="table table-striped table-bordered" >
                            <thead>
                                <tr>
                                    <th scope="col">Doctor Name</th>
                                    <th scope="col">Department</th>
                                    <th scope="col">Doctor Availibilty</th>
                                    <th scope="col">View Doctor</th>
                                    
                                </tr>
                            </thead>

                            <div v-if="filteredDoctors.length === 0" class="text-center p-3">No matching doctors found.</div>
                            <tbody v-else>
                                <tr v-for="doctor in filteredDoctors" :key="doctor.id">
                                    <td>{{ doctor.name }}</td>
                                    <td>{{ doctor.department_name }}</td>
                                    <td><RouterLink :to="{ name: 'Appointment', params: { department: doctor.department_name, doctor_id: doctor.id } }"><button>Check Availability</button></RouterLink></td>
                                    <td><RouterLink :to="{ name: 'Doctor_details', params: { id: doctor.id } }"><button>View details</button></RouterLink></td>
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
    name: "Search",
    data() {
        return {
            token:"",
            doctors: [],
            overview:"",
            dept_name:"",
            searchTerm: "",
            searchKey: "doctor",
            // search: false,
            
        };
    },
    mounted(){
        this.tokenload()
        this.loadDoctors()

    }
    ,
    methods:{
        tokenload(){
            const token = localStorage.getItem("token");
            if (token){
                this.token = token;
            }
        },
        loadDoctors(){
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
                    
                    this.doctors = res.data.doctors;
            }).catch(err => this.error = err.response.data.message)
        },
    },
    computed: {
        filteredDoctors() {
            if (!this.searchTerm.trim()) return this.doctors;  
            if (this.searchKey === "doctor") {
                return this.doctors.filter(doctor => doctor.name.toLowerCase().includes(this.searchTerm.toLowerCase()));
            } else if (this.searchKey === "department") {
                return this.doctors.filter(doctor => doctor.department_name.toLowerCase().includes(this.searchTerm.toLowerCase()));
            }
            return this.doctors;  // Fallback
        }
    }
}


</script> 
