<template>
<div class="department-details-container">
    <!-- BACK BUTTON -->
    
    
    <div class="page-header">
        <h2>Department: {{ dept_name }}</h2>
    </div>
    
    <!-- Department Overview -->
    <div class="overview-card">
        <div class="overview-header">
            <h3>Overview</h3>
        </div>
        <div class="overview-content">
            <p>{{ overview || 'No overview available.' }}</p>
        </div>
    </div>
    
    <!-- Doctors Table -->
    <div class="doctors-card">
        <div class="section-header">
            <h3>Doctor's List</h3>
        </div>
        <div class="table-wrapper">
            <table class="doctors-table">
                <thead class="table-header">
                    <tr>
                        <th>Doctor Name</th>
                        <th>Availability</th>
                        <th>View Doctor</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="doctors.length === 0">
                        <td colspan="3" class="no-data">No doctors available in this department.</td>
                    </tr>
                    <tr v-else v-for="doctor in doctors" :key="doctor.id" class="doctor-row">
                        <td>{{ doctor.name }}</td>
                        <td>
                            <RouterLink :to="{ name: 'Appointment', params: { department: dept_name, doctor_id: doctor.id } }" class="btn-availability">
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
    <div class="back-button-container mt-5">
        <RouterLink to="/patient_dash" class="back-btn">
            <i class="bi bi-arrow-left"></i>
            Back to Dashboard
        </RouterLink>
    </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
    name: "DepartmentDetails",
    data() {
        return {
            token: "",
            user_type: "",
            doctors: [],
            overview: "",
            dept_name: "",
            error: ""
        };
    },
    mounted() {
        this.tokenload();
        this.department_details();
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        department_details() {
            const dept_id = this.$route.params.id;
            axios.get(`http://127.0.0.1:5000/api/department_doctors/${dept_id}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.doctors = res.data.doctors || [];
                this.overview = res.data.department_views?.overview || '';
                this.dept_name = res.data.department_views?.name || '';
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load department details';
                console.error(this.error);
            });
        }
    }
}
</script>

<style scoped>
.back-button-container {
    margin-bottom: 1.5rem;
    text-align: left;
}

.back-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    border: 2px solid rgba(16, 185, 129, 0.2);
}

.back-btn:hover {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}


.department-details-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
    padding: 2rem;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.page-header {
    text-align: center;
    margin-bottom: 2.5rem;
}

.page-header h2 {
    color: #581c87;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.overview-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    border: 1px solid rgba(139,92,246,0.2);
    margin-bottom: 2rem;
}

.overview-header {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 16px 16px 0 0;
    margin: -2rem -2rem 1.5rem -2rem;
}

.overview-header h3 {
    margin: 0;
    font-size: 1.3rem;
    font-weight: 700;
}

.overview-content {
    color: #581c87;
    line-height: 1.7;
    font-size: 1.1rem;
}

.doctors-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    border: 1px solid rgba(139,92,246,0.2);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.section-header {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    padding: 1.5rem 2rem;
    flex-shrink: 0;
}

.section-header h3 {
    margin: 0;
    font-size: 1.4rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-header h3::before {
    content: '';
    width: 4px;
    height: 24px;
    background: rgba(255,255,255,0.3);
    border-radius: 2px;
}

.table-wrapper {
    flex: 1;
    overflow: hidden;
    position: relative;
}

.doctors-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.table-header {
    position: sticky;
    top: 0;
    z-index: 100;
}

.table-header th {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: white !important;
    padding: 1.25rem 1rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-bottom: 3px solid rgba(255,255,255,0.2) !important;
}

.doctors-table td {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid rgba(139,92,246,0.1);
    color: #581c87;
    vertical-align: middle;
}

.doctor-row {
    transition: all 0.3s ease;
}

.doctor-row:hover {
    background: rgba(139,92,246,0.08);
    transform: translateY(-1px);
}

.btn-availability, .btn-details {
    padding: 0.6rem 1.4rem;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.btn-availability {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
}

.btn-availability:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16,185,129,0.4);
    color: white;
}

.btn-details {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    margin-left: 0.5rem;
}

.btn-details:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
    color: white;
}

.no-data {
    text-align: center;
    color: #6b7280;
    font-style: italic;
    padding: 3rem 1rem;
    font-size: 1.1rem;
}

/* Custom Scrollbar */
.table-wrapper::-webkit-scrollbar {
    width: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
    background: rgba(248,250,252,0.5);
    border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
}

@media (max-width: 768px) {
    .department-details-container {
        padding: 1rem;
    }
    
    .back-button-container {
        margin-bottom: 1rem;
    }
    
    .overview-card {
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .overview-header {
        padding: 0.875rem 1.25rem;
        margin: -1.5rem -1.5rem 1.25rem -1.5rem;
    }
    
    .doctors-card {
        border-radius: 16px;
    }
    
    .section-header {
        padding: 1.25rem 1.5rem;
    }
    
    .doctors-table {
        font-size: 0.9rem;
    }
    
    .doctors-table th,
    .doctors-table td {
        padding: 1rem 0.75rem;
    }
    
    .btn-availability, .btn-details {
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        display: block;
        margin: 0.25rem 0;
    }
    
    .btn-details {
        margin-left: 0 !important;
    }
}
</style>
