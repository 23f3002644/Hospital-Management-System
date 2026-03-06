<template>
<div class="patient-dashboard">
    <div class="page-header">
        <div class="header-content">
            <div>
                <h2>Patient Dashboard</h2>
            </div>
        </div>
    </div>

    <div class="dashboard-grid">
        <!-- Departments -->
        <div class="card-section">
            <div class="section-header">
                <h3>Departments</h3>
            </div>
            <div class="table-wrapper">
                <table class="dashboard-table">
                    <thead class="table-header">
                        <tr>
                            <th>Department Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="!departments || departments.length === 0">
                            <td colspan="2" class="no-data">No departments available</td>
                        </tr>
                        <tr v-else v-for="depart in departments" :key="depart.id">
                            <td>{{ depart.name }}</td>
                            <td>
                                <RouterLink :to="`/department_details/${depart.id}`" class="btn-view">
                                    View Details
                                </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Upcoming Appointments -->
        <div class="card-section">
            <div class="section-header">
                <h3>Upcoming Appointments</h3>
            </div>
            <div class="table-wrapper">
                <table class="dashboard-table">
                    <thead class="table-header">
                        <tr>
                            <th>Doctor Name</th>
                            <th>Department</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="!appointments || appointments.length === 0">
                            <td colspan="5" class="no-data">No upcoming appointments</td>
                        </tr>
                        <tr v-else v-for="appointment in appointments" :key="appointment.id">
                            <td>{{ appointment.doctor_name }}</td>
                            <td>{{ appointment.department_name }}</td>
                            <td>{{ appointment.date }}</td>
                            <td>{{ appointment.time }}</td>
                            <td>
                                <button class="btn-cancel" @click="cancelAppointment(appointment.id)">
                                    Cancel
                                </button>
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
    name: "PatientDashboard",
    data() {
        return {
            token: "",
            user_type: "",
            appointments: [],
            departments: [],
            error: ""
        };
    },
    mounted() {
        this.tokenload();
        this.loggingdashboard();
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        loggingdashboard() {
            axios.get("http://127.0.0.1:5000/api/patient_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.departments = res.data.departments || [];
                this.appointments = res.data.appointments || [];
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load dashboard';
                console.error(this.error);
            });
        },
        cancelAppointment(appointmentId) {
            if (confirm('Are you sure you want to cancel this appointment?')) {
                axios.put(`http://127.0.0.1:5000/api/cancel_appointment/${appointmentId}`, {}, {
                    headers: { "Authentication-Token": this.token }
                })
                .then(() => {
                    this.appointments = this.appointments.filter(app => app.id !== appointmentId);
                })
                .catch(err => {
                    console.error('Cancel failed:', err.response?.data);
                });
            }
        }
    }
}
</script>

<style scoped>
.patient-dashboard {
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

.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

.card-section {
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
    background: linear-gradient(135deg, #10b981, #059669);
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

.dashboard-table {
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
    background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
    color: white !important;
    padding: 1.25rem 1rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-bottom: 3px solid rgba(255,255,255,0.2) !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 50 !important;
}

.dashboard-table td {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid rgba(139,92,246,0.1);
    color: #581c87;
    vertical-align: middle;
    word-break: break-word;
}

.dashboard-table tbody tr {
    transition: all 0.3s ease;
}

.dashboard-table tbody tr:hover {
    background: rgba(139,92,246,0.08);
    transform: translateY(-1px);
}

.btn-view, .btn-cancel {
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

.btn-view {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
}

.btn-view:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4);
    color: white;
}

.btn-cancel {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
}

.btn-cancel:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(239,68,68,0.4);
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
    .patient-dashboard {
        padding: 1rem;
    }
    
    .dashboard-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .card-section {
        border-radius: 16px;
    }
    
    .section-header {
        padding: 1.25rem 1.5rem;
    }
    
    .dashboard-table {
        font-size: 0.9rem;
    }
    
    .dashboard-table th,
    .dashboard-table td {
        padding: 1rem 0.75rem;
    }
    
    .btn-view, .btn-cancel {
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
    }
}
</style>
