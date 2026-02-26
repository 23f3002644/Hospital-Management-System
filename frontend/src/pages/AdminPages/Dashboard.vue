<template>
<div>
    <div class="dashboard-stats mb-5 mt-4">
    <!-- ROW 1: Patients + Doctors + Appointments -->
    <div class="row g-4 mb-4">
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 bg-primary text-white rounded shadow">
                <i class="fas fa-user-md fa-3x mb-3"></i>
                <h3 class="mb-2">Total Patients</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalPatients }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 bg-success text-white rounded shadow">
                <i class="fas fa-stethoscope fa-3x mb-3"></i>
                <h3 class="mb-2">Total Doctors</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalDoctors }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 bg-info text-white rounded shadow">
                <i class="fas fa-calendar-check fa-3x mb-3"></i>
                <h3 class="mb-2">Total Appointments</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalAppointments }}</h2>
            </div>
        </div>
    </div>

    <!-- ROW 2: Upcoming + Departments + Treatments -->
    <div class="row g-4">
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 bg-warning text-dark rounded shadow">
                <i class="fas fa-clock fa-3x mb-3"></i>
                <h3 class="mb-2">Upcoming Appointments</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalUpcomingAppointments }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 bg-danger text-white rounded shadow">
                <i class="fas fa-building fa-3x mb-3"></i>
                <h3 class="mb-2">Total Departments</h3>
                <h2 class="display-4 fw-bold mb-0">{{ totalDepartments }}</h2>
            </div>
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="stat-card h-100 text-center p-4 bg-secondary text-white rounded shadow">
                <i class="fas fa-capsules fa-3x mb-3"></i>
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
        <div style="position: relative; height: 350px;">
            <canvas ref="appointmentStatusChart"></canvas>
        </div>
    </div>

    <!-- Chart 2 - Right -->
    <div class="chart-container" style="height: 400px; flex: 1; min-width: 300px; margin-bottom: 50px;">
        <h5 style="margin-bottom: 15px;">Doctor Distribution Chart</h5>
        <div style="position: relative; height: 350px;">
            <canvas ref="doctorDistributionChart"></canvas>
        </div>
    </div>
    </div>

</div>
</template>
<script>
import axios from 'axios';
import Appointment from '../Patients/Appointment.vue';
import {Chart}  from 'chart.js/auto';
import { render } from 'vue';

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
            // Debounce to prevent rapid re-renders
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
                doctorCounts[doc.department_name] = (doctorCounts[doc.name] || 0) + 1;
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
        },
        // statusOfAppointmenta(){
        //     const statusCounts = {};
        //     this.appointments.forEach(appointment => {
        //         const status = appointment.status;
        //         if (statusCounts[status]) {
        //             statusCounts[status]++;
        //         } else {
        //             statusCounts[status] = 1;
        //         }
        //     });
        //     return {
        //         labels: Object.keys(statusCounts),
        //         datasets: [{
        //             label: 'Number of Appointments by Status',
        //             data: Object.values(statusCounts),
        //             backgroundColor: 'rgba(75, 192, 192, 0.2)',
        //             borderColor: 'rgba(75, 192, 192, 1)',
        //             borderWidth: 1
        //         }]
        //     }
        // },
        // doctorDistribution(){
        //     const doctorCounts = {};
        //     this.doctors.forEach(doctor => {
        //         const department = doctor.department_name;
        //         if (doctorCounts[department]) {
        //             doctorCounts[department]++;
        //         } else {
        //             doctorCounts[department] = 1;
        //         }
        //     });
        //     return {
        //         labels: Object.keys(doctorCounts),
        //         datasets: [{
        //             label: 'Number of Doctors per Department',
        //             data: Object.values(doctorCounts),
        //             backgroundColor: 'rgba(75, 192, 192, 0.2)',
        //             borderColor: 'rgba(75, 192, 192, 1)',
        //             borderWidth: 1
        //         }]
        //     }
        // }

}
}

</script>
<style scoped>
.stat-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
    cursor: pointer;
}

.stat-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.2) !important;
}

.display-4 {
    font-size: 2.5rem;
    font-weight: 700;
}

@media (max-width: 768px) {
    .display-4 {
        font-size: 2rem;
    }
    .stat-card {
        margin-bottom: 1rem;
    }
}
</style>
