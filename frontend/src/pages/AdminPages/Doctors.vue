<template>
    
                    
<div class="container mt-5">
            <div class="row">
                <div class="col-md-12">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2 style="text-align: center;">Registered Doctors</h2>
                    <RouterLink to="/add_doctor" class="btn btn-success">Add Doctor</RouterLink>
                    </div>


                    <div>
                    <h4 class="heading mt-2 text-center">Filter Here</h4>
                        <form class="d-flex mt-4" >
                        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model.trim="searchTerm" name="value">
                        <select class="form-select me-2" aria-label="Search by" v-model="searchKey" name="key">
                            <option value="doctor">Doctor Name</option>
                            <option value="department">Department</option>
                        </select>
                        </form>
                    </div>



                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Doctor Name</th>
                                    <th scope="col">Gender</th>
                                    <th scope="col">Age</th>
                                    <th scope="col">Specialty</th>
                                    <th scope="col">Department</th>
                                    <th scope="col">Description</th>
                                    <th scope="col">Address</th>
                                    <th scope="col">Contact Number</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody v-if="filteredDoctors.length === 0">
                                <tr>
                                    <td colspan="9" class="text-center">No doctors found.</td>
                                </tr>
                            </tbody>
                            <tbody v-else>
                                <tr v-for="doctor in filteredDoctors" :key="doctor.id">
                                    <td>{{ doctor.name }}</td>
                                    <td>{{ doctor.gender }}</td>
                                    <td>{{ doctor.age }}</td>
                                    <td>{{ doctor.specialty }}</td>
                                    <td>{{ doctor.department_name }}</td>
                                    <td>{{ doctor.description }}</td>
                                    <td>{{ doctor.address }}</td>
                                    <td>{{ doctor.contact_number }}</td>
                                    <td>
                                   <RouterLink :to="`/edit_doctor/${doctor.id}`" class="btn btn-outline-danger me-2">Edit</RouterLink>
                                    <button class="btn btn-danger me-2" @click="deleteDoctor(doctor.id)">Delete</button>
                                    <button v-if="doctor.active" class="btn btn-secondary me-2" @click="blacklist(doctor.id)">Blacklist</button>
                                    <button v-else class="btn btn-success me-2" @click="unblacklist(doctor.id)">Unblacklist</button>
                                    <!-- <button class="btn btn-secondary me-2" @click="blacklist(doctor.id)">Blacklist</button> -->
                                </td>
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
    name: "Doctor_dash",
    data() {
        return {
            token:"",
            user_type:"",
            doctors: [],
            searchTerm: "",
            searchKey: "doctor",
            // Data properties can be added here if needed
        };
    },
    mounted(){
            this.tokenload()
            this.doctorLoad()
            // this.fetchAppointments()
            // this.fetchPatients()

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
        doctorLoad(){
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
                    this.doctors = res.data.doctors;
            }).catch(err => this.error = err.response.data.message)
        },
        deleteDoctor(doctor_id) {
            const response = axios.delete(`http://127.0.0.1:5000/api/delete_doctor/${doctor_id}`, {
            headers: { "Authentication-Token": this.token }
            })
            response
            .then(res => {
            // console.log('Success:', res.data);
            // Remove the deleted doctor from the list
            this.doctors = this.doctors.filter(doctor => doctor.id !== doctor_id);
            // console.log('Doctor deleted successfully');
            })
            .catch(err => {
            console.error('Status:', err.response?.status);  // 401
            console.error('Error:', err.response?.data);     // {"message": "Invalid token"}
            });
        },
        blacklist(doctor_id) {
            const response = axios.put(`http://127.0.0.1:5000/api/blacklist_doctor/${doctor_id}`, null, {
                headers: { "Authentication-Token": this.token }
            })
            response
            .then(res => {
                this.doctorLoad();  // Refresh the doctor list to reflect the change
                // console.log('Doctor blacklisted successfully');
            })
            .catch(err => {
                console.error('Error blacklisting doctor:', err.response?.data);
            });
        },
        unblacklist(doctor_id) {
            const response = axios.put(`http://127.0.0.1:5000/api/unblacklist_doctor/${doctor_id}`, null, {
                headers: { "Authentication-Token": this.token }
            })
            response
            .then(res => {
                this.doctorLoad();  // Refresh the doctor list to reflect the change
                // console.log('Doctor unblacklisted successfully');
            })
            .catch(err => {
                console.error('Error unblacklisting doctor:', err.response?.data);
            });

    }
     },
    computed: {
        filteredDoctors() {
            if (!this.searchTerm.trim()) return this.doctors;  // Show all if empty search
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