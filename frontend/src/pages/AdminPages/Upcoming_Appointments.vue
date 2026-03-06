<template>
<div class="appointments-container">
    <div class="page-header">
        <h2>Upcoming Appointments</h2>
    </div>
    
    <div class="table-container">
        <div class="table-responsive">
            <table class="appointments-table">
                <thead>
                    <tr>
                        <th>Patient Name</th>
                        <th>Doctor Name</th>
                        <th>Department</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Patient History</th>
                    </tr>
                </thead>
                <tbody v-if="appointments.length === 0">
                    <tr>
                        <td colspan="6" class="no-data">No upcoming appointments found.</td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr v-for="appointment in upcomingAppointments" :key="appointment.id" class="appointment-row">
                        <td>{{ appointment.patient_name }}</td>
                        <td>{{ appointment.doctor_name }}</td>
                        <td>{{ appointment.department_name }}</td>
                        <td>{{ formatDate(appointment.date) }}</td>
                        <td>{{ appointment.time }}</td>
                        <td>
                            <RouterLink class="history-btn" :to="`/patient/history/${appointment.patient_id}`">
                                View History
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
    name: "Upcoming_Appointments",
    data() {
        return {
            token: "",
            user_type: "",
            appointments: [],
            error: ""
        };
    },
    computed: {
        upcomingAppointments() {
            return this.appointments.filter(appointment => appointment.status === 'booked');
        }
    },
    mounted() {
        this.tokenload();
        this.upcomingAppointment();
    },
    methods: {
        tokenload() {
            const token = localStorage.getItem("token");
            if (token) {
                this.token = token;
            }
            const user_type = localStorage.getItem('user_type');
            if (user_type) {
                this.user_type = user_type;
            }
        },
        upcomingAppointment() {
            const response = axios.get("http://127.0.0.1:5000/api/admin_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.appointments = res.data.appointments || [];
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load appointments';
                console.error(this.error);
            });
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleDateString('en-IN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        }
    }
}
</script>

<style scoped>
.appointments-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
    padding: 2rem;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.page-header {
    text-align: center;
    margin-bottom: 3rem;
}

.page-header h2 {
    color: #581c87;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
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

.table-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    border: 1px solid rgba(139,92,246,0.2);
}

.appointments-table {
    width: 100%;
    border-collapse: collapse;
    margin: 0;
}

.appointments-table th {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    padding: 1.25rem 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.appointments-table td {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid rgba(139,92,246,0.1);
    color: #581c87;
}

.appointment-row:hover {
    background: rgba(139,92,246,0.05);
    transform: scale(1.01);
}

.appointment-row td:last-child {
    white-space: nowrap;
}

.history-btn {
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 12px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(139,92,246,0.3);
}

.history-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(139,92,246,0.4);
    color: white;
    text-decoration: none;
}

.no-data {
    text-align: center;
    color: #6b7280;
    font-style: italic;
    padding: 3rem;
    font-size: 1.1rem;
}

@media (max-width: 768px) {
    .appointments-container {
        padding: 1rem;
    }
    
    .table-container {
        padding: 1.5rem;
        margin: 0;
    }
    
    .page-header h2 {
        font-size: 2rem;
    }
    
    .appointments-table {
        font-size: 0.9rem;
    }
    
    .appointments-table th,
    .appointments-table td {
        padding: 0.75rem 0.5rem;
    }
    
    .history-btn {
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
    }
}
</style>
