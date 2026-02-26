<template>
<div class="container mt-5">
            <div class="row">
                <div class="col-md-12">
                    <h2>Registered Patients</h2>


        <div>
            <h4 class="heading mt-2 text-center">Filter Here</h4>
            <form class="d-flex mt-4" >
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model.trim="searchTerm" name="value">
                    <select class="form-select me-2" aria-label="Search by" v-model="searchKey" name="key">
                        <option value="name">Patient Name</option>
                        <option value="address">Address</option>
                    </select>
            </form>
        </div>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Patient Name</th>
                                    <th scope="col">Gender</th>
                                    <th scope="col">Age</th>
                                    <th scope="col">Address</th>
                                    <th scope="col">Contact Number</th>
                                    <th scope="col">Action</th>
                                </tr>
                            </thead>
                            <div v-if="filteredPatients && filteredPatients.length === 0" colspan="6" class="text-center p-3">No matching patients found.</div>
                            <tbody v-else>
                                <tr v-for="patient in filteredPatients" :key="patient.id">
                                    <td>{{ patient.name }}</td>
                                    <td>{{ patient.gender }}</td>
                                    <td>{{ patient.age }}</td>
                                    <td>{{ patient.address }}</td>
                                    <td>{{ patient.contact_number }}</td>
                                    <td>
                                    <button class="btn btn-danger me-2" @click="deletePatient(patient.id)">Delete</button>
                                    <button v-if="patient.active" class="btn btn-secondary me-2" @click="blacklist(patient.id)">Blacklist</button>
                                    <button v-else class="btn btn-success me-2" @click="unblacklist(patient.id)">Unblacklist</button>
                                    <!-- <button class="btn btn-secondary me-2" @click="blacklist(patient.id)">Blacklist</button> -->
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
            appointments: [],
            patients: [],
            searchTerm: "",
            searchKey: "name"
        };
    },
    mounted(){
            this.tokenload()
            this.patientLoad()
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
        patientLoad(){
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
                    this.patients = res.data.patients;
            }).catch(err => this.error = err.response.data.message)
        },
        deletePatient(patient_id) {
            const response = axios.delete(`http://127.0.0.1:5000/api/delete_patient/${patient_id}`, {
            headers: { "Authentication-Token": this.token }
            })
            response
            .then(res => {
            // console.log('Success:', res.data);
            // Remove the deleted patient from the list
            this.patients = this.patients.filter(patient => patient.id !== patient_id);
            // console.log('Patient deleted successfully');
            })
            .catch(err => {
            console.error('Status:', err.response?.status);  // 401
            console.error('Error:', err.response?.data);     // {"message": "Invalid token"}
            });
        },
        blacklist(patient_id) {
            const response = axios.put(`http://127.0.0.1:5000/api/blacklist_patient/${patient_id}`, null, {
                headers: { "Authentication-Token": this.token }
            })
            response
            .then(res => {
                this.patientLoad();  // Refresh the patient list to reflect the change
                // console.log('Patient blacklisted successfully');
            })
            .catch(err => {
                console.error('Error blacklisting patient:', err.response?.data);
            });
        },
        unblacklist(patient_id) {
            const response = axios.put(`http://127.0.0.1:5000/api/unblacklist_patient/${patient_id}`, null, {
                headers: { "Authentication-Token": this.token }
            })
            response
            .then(res => {
                this.patientLoad(); // Reload patients list to reflect changes
                // console.log('Patient unblacklisted successfully');
            })
            .catch(err => {
                console.error('Error unblacklisting patient:', err.response?.data);
            });
        }
        },
    computed: {
        filteredPatients() {
            if (!this.searchTerm.trim()) return this.patients;  // Show all if empty search
            if (this.searchKey === "name") {
                return this.patients.filter(patient => patient.name.toLowerCase().includes(this.searchTerm.toLowerCase()));
            } else if (this.searchKey === "address") {
                return this.patients.filter(patient => patient.address.toLowerCase().includes(this.searchTerm.toLowerCase()));
            }
            return this.patients;  // Fallback
        }
    }

}
</script>