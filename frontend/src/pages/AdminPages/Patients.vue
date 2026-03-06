<template>
<div class="patients-container">
    <div class="page-header">
        <h2>Registered Patients</h2>
    </div>
    
    <div class="patients-card">
        <!-- Search Filter -->
        <div class="filter-section">
            <h4>Filter Patients</h4>
            <div class="search-form">
                <input class="search-input" type="search" placeholder="Search patients..." v-model.trim="searchTerm">
                <select class="search-select" v-model="searchKey">
                    <option value="name">Patient Name</option>
                    <option value="address">Address</option>
                </select>
            </div>
        </div>
        
        <!-- Patients Table -->
        <div class="table-responsive">
            <table class="patients-table">
                <thead>
                    <tr>
                        <th>Patient Name</th>
                        <th>Gender</th>
                        <th>Age</th>
                        <th>Address</th>
                        <th>Contact Number</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="filteredPatients.length === 0">
                        <td colspan="6" class="no-data">
                            {{ searchTerm ? 'No matching patients found.' : 'No patients registered yet.' }}
                        </td>
                    </tr>
                    <tr v-else v-for="patient in filteredPatients" :key="patient.id" class="patient-row">
                        <td>{{ patient.name }}</td>
                        <td>{{ patient.gender }}</td>
                        <td>{{ patient.age }}</td>
                        <td>{{ patient.address }}</td>
                        <td>{{ patient.contact_number }}</td>
                        <td class="action-buttons">
                            <button class="btn-delete" @click="deletePatient(patient.id)">Delete</button>
                            <button class="btn-blacklist" :class="{ 'btn-unblacklist': !patient.active }"
                                @click="patient.active ? blacklist(patient.id) : unblacklist(patient.id)">
                                {{ patient.active ? 'Blacklist' : 'Unblacklist' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
    name: "RegisteredPatients",
    data() {
        return {
            token: "",
            user_type: "",
            patients: [],
            searchTerm: "",
            searchKey: "name",
            error: ""
        };
    },
    mounted() {
        this.tokenload();
        this.patientLoad();
    },
    computed: {
        filteredPatients() {
            // find out the usage of trim
            if (!this.searchTerm.trim()) return this.patients;  
            if (this.searchKey === "name") {
                return this.patients.filter(patient => 
                    patient.name.toLowerCase().includes(this.searchTerm.toLowerCase())
                );
            } else if (this.searchKey === "address") {
                return this.patients.filter(patient => 
                    patient.address.toLowerCase().includes(this.searchTerm.toLowerCase())
                );
            }
            return this.patients;
        }
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        patientLoad() {
            axios.get("http://127.0.0.1:5000/api/admin_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.patients = res.data.patients || [];
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load patients';
                console.error(this.error);
            });
        },
        deletePatient(patient_id) {
            if (confirm('Are you sure you want to delete this patient?')) {
                axios.delete(`http://127.0.0.1:5000/api/delete_patient/${patient_id}`, {
                    headers: { "Authentication-Token": this.token }
                })
                .then(() => {
                    this.patients = this.patients.filter(patient => patient.id !== patient_id);
                })
                .catch(err => console.error('Delete failed:', err.response?.data));
            }
        },
        blacklist(patient_id) {
            axios.put(`http://127.0.0.1:5000/api/blacklist_patient/${patient_id}`, null, {
                headers: { "Authentication-Token": this.token }
            })
            .then(() => this.patientLoad())
            .catch(err => console.error('Blacklist failed:', err.response?.data));
        },
        unblacklist(patient_id) {
            axios.put(`http://127.0.0.1:5000/api/unblacklist_patient/${patient_id}`, null, {
                headers: { "Authentication-Token": this.token }
            })
            .then(() => this.patientLoad())
            .catch(err => console.error('Unblacklist failed:', err.response?.data));
        }
    }
}
</script>

<style scoped>
.patients-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
    padding: 2rem;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.page-header {
    text-align: center;
    margin-bottom: 2rem;
}

.page-header h2 {
    color: #581c87;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-header p {
    color: #6b21a8;
    font-size: 1.1rem;
    margin: 0;
}

.patients-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    border: 1px solid rgba(139,92,246,0.2);
}

.filter-section {
    margin-bottom: 2rem;
}

.filter-section h4 {
    color: #581c87;
    margin-bottom: 1rem;
    font-weight: 600;
}

.search-form {
    display: flex;
    gap: 1rem;
    max-width: 500px;
    margin: 0 auto;
}

.search-input, .search-select {
    flex: 1;
    padding: 0.875rem 1.25rem;
    border: 2px solid rgba(139,92,246,0.2);
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.9);
}

.search-input:focus, .search-select:focus {
    outline: none;
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1);
    transform: translateY(-1px);
}

.patients-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.patients-table th {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    padding: 1.25rem 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.patients-table td {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid rgba(139,92,246,0.1);
    color: #581c87;
    vertical-align: middle;
}

.patient-row:hover {
    background: rgba(139,92,246,0.05);
}

.action-buttons {
    white-space: nowrap;
}

.btn-delete, .btn-blacklist, .btn-unblacklist {
    padding: 0.5rem 1.25rem;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-right: 0.5rem;
}

.btn-delete {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
}

.btn-delete:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(239,68,68,0.4);
}

.btn-blacklist {
    background: linear-gradient(135deg, #6b7280, #4b5563);
    color: white;
}

.btn-blacklist:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(107,114,128,0.4);
}

.btn-unblacklist {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
}

.btn-unblacklist:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(16,185,129,0.4);
}

.no-data {
    text-align: center;
    color: #6b7280;
    font-style: italic;
    padding: 3rem 1rem;
    font-size: 1.1rem;
}

@media (max-width: 768px) {
    .patients-container {
        padding: 1rem;
    }
    
    .patients-card {
        padding: 1.5rem;
        margin: 0;
    }
    
    .search-form {
        flex-direction: column;
    }
    
    .patients-table {
        font-size: 0.9rem;
    }
    
    .patients-table th,
    .patients-table td {
        padding: 0.75rem 0.5rem;
    }
    
    .action-buttons {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .btn-delete, .btn-blacklist, .btn-unblacklist {
        width: 100%;
        margin-right: 0;
        margin-bottom: 0.25rem;
    }
}
</style>
