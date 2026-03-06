<template>
<div class="doctors-container">
    <div class="page-header">
        <h2>Doctor's List</h2>
    </div>
    
    <div class="doctors-card">
        <!-- Search Filter -->
        <div class="filter-section">
            <h4>Filter Doctors</h4>
            <div class="search-form">
                <input class="search-input" type="search" placeholder="Search doctors..." v-model.trim="searchTerm">
                <select class="search-select" v-model="searchKey">
                    <option value="doctor">Doctor Name</option>
                    <option value="department">Department</option>
                </select>
            </div>
        </div>
        
        <!-- Doctors Table -->
        <div class="table-responsive">
            <table class="doctors-table">
                <thead>
                    <tr>
                        <th>Doctor Name</th>
                        <th>Department</th>
                        <th>Availability</th>
                        <th>View Doctor</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="filteredDoctors.length === 0">
                        <td colspan="4" class="no-data">
                            {{ searchTerm ? 'No matching doctors found.' : 'No doctors available.' }}
                        </td>
                    </tr>
                    <tr v-else v-for="doctor in filteredDoctors" :key="doctor.id" class="doctor-row">
                        <td>{{ doctor.name }}</td>
                        <td>{{ doctor.department_name }}</td>
                        <td>
                            <RouterLink :to="{ name: 'Appointment', params: { department: doctor.department_name, doctor_id: doctor.id } }" class="btn-availability">
                                Check Availability
                            </RouterLink>
                        </td>
                        <td>
                            <RouterLink :to="{ name: 'Doctor_details', params: { id: doctor.id } }" class="btn-details">
                                View Details
                            </RouterLink>
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
    name: "DoctorSearch",
    data() {
        return {
            token: "",
            user_type: "",
            doctors: [],
            searchTerm: "",
            searchKey: "doctor",
            error: ""
        };
    },
    mounted() {
        this.tokenload();
        this.loadDoctors();
    },
    computed: {
        filteredDoctors() {
            if (!this.searchTerm.trim()) return this.doctors;
            if (this.searchKey === "doctor") {
                return this.doctors.filter(doctor => 
                    doctor.name.toLowerCase().includes(this.searchTerm.toLowerCase())
                );
            } else if (this.searchKey === "department") {
                return this.doctors.filter(doctor => 
                    doctor.department_name.toLowerCase().includes(this.searchTerm.toLowerCase())
                );
            }
            return this.doctors;
        }
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        loadDoctors() {
            axios.get("http://127.0.0.1:5000/api/patient_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.doctors = res.data.doctors || [];
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load doctors';
                console.error(this.error);
            });
        }
    }
}
</script>

<style scoped>
.doctors-container {
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

.doctors-card {
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

.doctors-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.doctors-table th {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    padding: 1.25rem 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.doctors-table td {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid rgba(139,92,246,0.1);
    color: #581c87;
    vertical-align: middle;
}

.doctor-row:hover {
    background: rgba(139,92,246,0.05);
}

.btn-availability, .btn-details {
    padding: 0.5rem 1.25rem;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    margin-right: 0.5rem;
}

.btn-availability {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
}

.btn-availability:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(16,185,129,0.4);
    color: white;
}

.btn-details {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
}

.btn-details:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(59,130,246,0.4);
    color: white;
}

.no-data {
    text-align: center;
    color: #6b7280;
    font-style: italic;
    padding: 3rem 1rem;
    font-size: 1.1rem;
}

@media (max-width: 768px) {
    .doctors-container {
        padding: 1rem;
    }
    
    .doctors-card {
        padding: 1.5rem;
        margin: 0;
    }
    
    .search-form {
        flex-direction: column;
    }
    
    .doctors-table {
        font-size: 0.9rem;
    }
    
    .doctors-table th,
    .doctors-table td {
        padding: 0.75rem 0.5rem;
    }
    
    .btn-availability, .btn-details {
        width: 100%;
        margin-right: 0;
        margin-bottom: 0.25rem;
    }
}
</style>
