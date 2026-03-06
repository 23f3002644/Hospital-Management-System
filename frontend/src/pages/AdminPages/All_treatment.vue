<template>
<div class="doctors-container">
    <div class="page-header">
        <div class="header-content">
            <div>
                <h2>All Treatments</h2>
            </div>
        </div>
    </div>
    
    <div class="treatments-card">
        <!-- Search Filter -->
        <div class="filter-section">
            <h4>Filter Treatments</h4>
            <div class="search-form">
                <input class="search-input" type="search" placeholder="Search treatments..." v-model.trim="searchTerm">
                <select class="search-select" v-model="searchKey">
                    <option value="patient">Patient Name</option>
                    <option value="doctor">Doctor Name</option>
                    <option value="department">Department</option>
                    <option value="date">Date</option>
                </select>
            </div>
        </div>
        
        <!-- Treatments Table -->
        <div class="table-responsive">
            <table class="treatments-table">
                <thead>
                    <tr>
                        <th>Patient</th>
                        <th>Doctor</th>
                        <th>Department</th>
                        <th>Diagnosis</th>
                        <th>Test</th>
                        <th>Prescription</th>
                        <th>Medicines</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Type</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="filteredTreatments.length === 0">
                        <td colspan="11" class="no-data">
                            {{ searchTerm ? 'No matching treatments found.' : 'No treatments available.' }}
                        </td>
                    </tr>
                    <tr v-else v-for="treatment in filteredTreatments" :key="treatment.id" class="treatment-row">
                        <td>{{ treatment.patient_name }}</td>
                        <td>{{ treatment.doctor_name }}</td>
                        <td>{{ treatment.department_name }}</td>
                        <td class="scroll-cell">{{ treatment.diagnosis }}</td>
                        <td class="scroll-cell">{{ treatment.test_done }}</td>
                        <td class="scroll-cell">{{ treatment.prescription }}</td>
                        <td class="scroll-cell">{{ treatment.medicines }}</td>
                        <td>{{ treatment.date }}</td>
                        <td>{{ treatment.time }}</td>
                        <td>{{ treatment.visit_type }}</td>
                        <td class="scroll-cell">{{ treatment.notes }}</td>
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
    name: "AllTreatments",
    data() {
        return {
            token: "",
            user_type: "",
            treatments: [],
            searchTerm: "",
            searchKey: "patient",
            error: ""
        };
    },
    mounted() {
        this.tokenload();
        this.treatmentLoad();
    },
    computed: {
        filteredTreatments() {
            if (!this.searchTerm.trim()) return this.treatments;
            const term = this.searchTerm.toLowerCase();
            if (this.searchKey === "patient") {
                return this.treatments.filter(treatment => 
                    treatment.patient_name.toLowerCase().includes(term)
                );
            } else if (this.searchKey === "doctor") {
                return this.treatments.filter(treatment => 
                    treatment.doctor_name.toLowerCase().includes(term)
                );
            } else if (this.searchKey === "department") {
                return this.treatments.filter(treatment => 
                    treatment.department_name.toLowerCase().includes(term)
                );
            } else if (this.searchKey === "date") {
                return this.treatments.filter(treatment => 
                    treatment.date.toLowerCase().includes(term)
                );
            }
            return this.treatments;
        }
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        treatmentLoad() {
            axios.get("http://127.0.0.1:5000/api/admin_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.treatments = res.data.treatments || [];
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load treatments';
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

.page-header p {
    color: #6b21a8;
    font-size: 1.1rem;
    margin: 0;
}

.treatments-card {
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

.treatments-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.treatments-table th {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    padding: 1.25rem 1rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Add this to your existing <style scoped> - ONLY CSS changes */

.treatments-table td {
    padding: 1.25rem 1rem;
    border-bottom: 1px solid rgba(139,92,246,0.1);
    color: #581c87;
    vertical-align: middle;
    max-width: 150px;           /* Fixed width for all cells */
    overflow: hidden;           /* Hide overflow */
    position: relative;         /* For scroll positioning */
}

.treatments-table td.scroll-cell {
    max-width: 120px;           /* Smaller for long content */
    height: 60px;               /* Fixed height */
    overflow-y: auto;           /* Vertical scroll */
    overflow-x: hidden;         /* No horizontal scroll */
    scrollbar-width: thin;      /* Firefox thin scrollbar */
    scrollbar-color: #8b5cf6 #f3f4f6; /* Custom scrollbar */
}

.treatments-table td.scroll-cell::-webkit-scrollbar {
    width: 6px;                 /* Webkit scrollbar width */
}

.treatments-table td.scroll-cell::-webkit-scrollbar-track {
    background: #f3f4f6;
    border-radius: 3px;
}

.treatments-table td.scroll-cell::-webkit-scrollbar-thumb {
    background: #8b5cf6;
    border-radius: 3px;
}

.treatments-table td.scroll-cell::-webkit-scrollbar-thumb:hover {
    background: #7c3aed;
}

/* Apply scroll to specific long-content columns */
.treatment-row td:nth-child(4),  /* Diagnosis */
.treatment-row td:nth-child(5),  /* Test done */
.treatment-row td:nth-child(6),  /* Prescription */
.treatment-row td:nth-child(7),  /* Medicines */
.treatment-row td:nth-child(11) { /* Notes */
    max-width: 120px !important;
    height: 60px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    position: relative !important;
    padding-right: 0.5rem !important;
}


.treatment-row:hover {
    background: rgba(139,92,246,0.05);
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
    
    .treatments-card {
        padding: 1.5rem;
        margin: 0;
    }
    
    .search-form {
        flex-direction: column;
    }
    
    .treatments-table {
        font-size: 0.85rem;
    }
    
    .treatments-table th,
    .treatments-table td {
        padding: 0.75rem 0.5rem;
    }
}
</style>
