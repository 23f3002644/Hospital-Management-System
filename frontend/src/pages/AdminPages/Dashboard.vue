<template>
<div class="dashboard-container">
    <div class="dashboard-stats mb-5 mt-4">
    <!-- ROW 1: Patients + Doctors + Appointments -->
    <div class="row g-4 mb-4">
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 violet-primary text-white rounded shadow">
                <h3 class="mb-2">Total Patients</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalPatients }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 violet-success text-white rounded shadow">
                <h3 class="mb-2">Total Doctors</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalDoctors }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 violet-info text-white rounded shadow">
                <h3 class="mb-2">Total Appointments</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalAppointments }}</h2>
            </div>
        </div>
    </div>

    <!-- ROW 2: Upcoming + Departments + Treatments -->
    <div class="row g-4">
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 violet-warning text-white rounded shadow">
                <h3 class="mb-2">Upcoming Appointments</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalUpcomingAppointments }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 violet-danger text-white rounded shadow">
                <h3 class="mb-2">Total Departments</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalDepartments }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 violet-secondary text-white rounded shadow">
                <h3 class="mb-2">Total Treatments</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalTreatments }}</h2>
            </div>
        </div>
    </div>
</div>

    <div class="charts" style="display: flex; gap: 20px; flex-wrap: wrap;">
    <!-- Chart 1 - Left -->
    <div class="chart-container" style="height: 400px; flex: 1; min-width: 300px; margin-bottom: 50px;">
        <h5 style="margin-bottom: 15px;">Appointment Status Chart</h5>
        <div style="position: relative; height: 300px;">
            <canvas ref="appointmentStatusChart"></canvas>
        </div>
    </div>

    <!-- Chart 2 - Right -->
    <div class="chart-container" style="height: 400px; flex: 1; min-width: 300px; margin-bottom: 50px;">
        <h5 style="margin-bottom: 15px;">Doctor Distribution Chart</h5>
        <div style="position: relative; height: 300px;">
            <canvas ref="doctorDistributionChart"></canvas>
        </div>
    </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import {Chart}  from 'chart.js/auto';

export default {
    name: "AdminDashboard",
    data() {
        return {
            token: "",
            user_type: "",
            patients: [],
            doctors: [],
            appointments: [],
            departments: [],
            treatments: [],
            chart1: null,
            chart2: null,
            chartTimeout: null
        };
    },
    mounted() {
        this.tokenload()
        this.dashboardLoad()
    },
    watch: {
        appointments: {
            handler() {
                clearTimeout(this.chartTimeout);
                this.chartTimeout = setTimeout(() => {
                    this.$nextTick(() => this.renderCharts());
                }, 100);
            },
            deep: true
        },
        doctors: {
            handler() {
                clearTimeout(this.chartTimeout);
                this.chartTimeout = setTimeout(() => {
                    this.$nextTick(() => this.renderCharts());
                }, 100);
            },
            deep: true
        }
},
    methods: {
        tokenload() {
            const token = localStorage.getItem("token");
            if (token) {
                this.token = token;
            }
            const user_type = localStorage.getItem('user_type');
            if (user_type) {
                this.user_type = user_type
            }
        },
        dashboardLoad(){
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
                    this.doctors = res.data.doctors;
                    this.appointments = res.data.appointments;
                    this.departments = res.data.departments;
                    this.treatments = res.data.treatments;
            }).catch(err => this.error = err.response.data.message)
        },
        renderCharts() {
    try {
        // Destroy existing charts SAFELY
        if (this.chart1) {
            this.chart1.destroy();
            this.chart1 = null;
        }
        if (this.chart2) {
            this.chart2.destroy();
            this.chart2 = null;
        }

        // Chart 1: Appointments - with full safety checks
        const canvas1 = this.$refs.appointmentStatusChart;
        if (!canvas1) return; // Exit if canvas not ready
        
        const ctx1 = canvas1.getContext('2d');
        if (!ctx1 || this.appointments.length === 0) return;

        const statusCounts = {};
        this.appointments.forEach(apt => {
            if (apt.status) {
                statusCounts[apt.status] = (statusCounts[apt.status] || 0) + 1;
            }
        });

        // Only create if we have valid data
        if (Object.keys(statusCounts).length > 0) {
            this.chart1 = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: Object.keys(statusCounts),
                    datasets: [{
                        label: 'Appointments',
                        data: Object.values(statusCounts),
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true } },
                    animation: false  // ✅ Disable animation to prevent errors
                }
            });
        }

        // Chart 2: Doctors - with full safety checks
        const canvas2 = this.$refs.doctorDistributionChart;
        if (!canvas2) return;
        
        const ctx2 = canvas2.getContext('2d');
        if (!ctx2 || this.doctors.length === 0) return;

        const doctorCounts = {};
        this.doctors.forEach(doc => {
            if (doc.department_name) {
                doctorCounts[doc.department_name] = (doctorCounts[doc.department_name] || 0) + 1;
            }
        });

        // Only create if we have valid data
        if (Object.keys(doctorCounts).length > 0) {
            this.chart2 = new Chart(ctx2, {
                type: 'pie',
                data: {
                    labels: Object.keys(doctorCounts),
                    datasets: [{
                        data: Object.values(doctorCounts),
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                            '#9966FF', '#FF9F40', '#C9CBCF'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,  // ✅ Disable animation
                    plugins: {
                        legend: { position: 'right' }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Chart rendering error:', error);
    }
}


        },       
    computed: {
        totalPatients() {
            return this.patients.length;
        },
        totalDoctors() {
            return this.doctors.length;
        },
        totalAppointments() {
            return this.appointments.length;
        },
        totalUpcomingAppointments() {
            const status = "booked";
            return this.appointments.filter(appointment => appointment.status === status ).length;
        },
        totalDepartments() {
            return this.departments.length;
        },
        totalTreatments() {
            return this.treatments.length;
        }

}
}


</script>

<style scoped>
.dashboard-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
    padding: 2rem;
}

/* Replace Bootstrap colors with Blue-Violet theme */
.violet-primary {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
}

.violet-success {
    background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%) !important;
}

.violet-info {
    background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%) !important;
}

.violet-warning {
    background: linear-gradient(135deg, #c084fc 0%, #e879f9 100%) !important;
}

.violet-danger {
    background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%) !important;
}

.violet-secondary {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
}

.stat-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
    cursor: pointer;
    border-radius: 20px !important;
    backdrop-filter: blur(10px);
}

.stat-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 50px rgba(139,92,246,0.4) !important;
}

.display-4 {
    font-size: 2.5rem;
    font-weight: 700;
}

.chart-container {
    background: rgba(255,255,255,0.95) !important;
    backdrop-filter: blur(15px);
    border-radius: 20px !important;
    border: 1px solid rgba(139,92,246,0.3);
    padding: 2rem !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
    .display-4 {
        font-size: 2rem;
    }
    .stat-card {
        margin-bottom: 1rem;
    }
    .dashboard-container {
        padding: 1rem;
    }
}
</style>
