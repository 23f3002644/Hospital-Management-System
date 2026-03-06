<template>
<div class="treatment-page">
    <div class="page-header">
        <div class="header-content">
            <div>
                <h2>Treatment Details</h2>
            </div>
            <RouterLink to="/doctor_dash" class="back-btn">
                 Back to Dashboard
            </RouterLink>
        </div>
    </div>

    <!-- Patient Info Card -->
    <div class="patient-card">
        <div class="patient-info">
            <div class="patient-avatar">
                <i class="bi bi-person-fill"></i>
            </div>
            <div class="patient-details">
                <h4>{{ patient_name || 'Loading...' }}</h4>
                <p class="department">{{ Department_name || 'Loading department...' }}</p>
            </div>
        </div>
    </div>

    <!-- Treatment Form -->
    <div class="treatment-form-card">
        <form @submit.prevent="treatment" class="treatment-form">
            <div class="form-grid">
                <!-- Diagnosis & Tests -->
                <div class="form-group">
                    <label>Diagnosis</label>
                    <input type="text" v-model="formData.diagnosis" required 
                           placeholder="Enter diagnosis details">
                </div>
                
                <div class="form-group">
                    <label>Tests Done</label>
                    <input type="text" v-model="formData.test_done" required 
                           placeholder="List of tests performed">
                </div>

                <!-- Prescription & Medicines -->
                <div class="form-group">
                    <label>Prescription</label>
                    <input type="text" v-model="formData.prescription" required 
                           placeholder="Prescription instructions">
                </div>
                
                <div class="form-group">
                    <label>Medicines</label>
                    <input type="text" v-model="formData.medicines" required 
                           placeholder="Medicine names & dosage">
                </div>
            </div>

            <!-- Visit Type -->
            <div class="form-group full-width">
                <label>Visit Type</label>
                <select v-model="formData.visit_type" required>
                    <option value="">Select Visit Type</option>
                    <option value="first_time">First Time</option>
                    <option value="follow_up">Follow Up</option>
                </select>
            </div>

            <!-- Notes -->
            <div class="form-group full-width">
                <label>Additional Notes</label>
                <textarea v-model="formData.notes" rows="4" required 
                          placeholder="Additional observations or instructions..."></textarea>
            </div>

            <!-- Action Buttons -->
            <div class="form-actions">
                <button type="submit" class="btn-submit">
                    <i class="bi bi-check"></i> Submit Treatment
                </button>
                <RouterLink to="/doctor_dash" class="btn-cancel">
                    Cancel
                </RouterLink>
            </div>
        </form>
    </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
    name: "TreatmentForm",
    data() {
        return {
            token: "",
            user_type: "",
            formData: {
                diagnosis: "",
                test_done: "",
                prescription: "",
                medicines: "",
                visit_type: "",
                notes: ""
            },
            patient_name: "",
            Department_name: "",
            appointment_id: "",
            error: ""
        };
    },
    mounted() {
        this.tokenload();
        this.appointment_id = this.$route.params.id;
        this.loggingdashboard();
    },
    methods: {
        tokenload() {
            this.token = localStorage.getItem("token") || "";
            this.user_type = localStorage.getItem('user_type') || "";
        },
        treatment() {
            const id = this.$route.params.id;
            axios.post(`http://127.0.0.1:5000/api/treatment/${id}`, this.formData, {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                this.$router.push('/doctor_dash');
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to submit treatment';
                console.error(this.error);
            });
        },
        loggingdashboard() {
            axios.get("http://127.0.0.1:5000/api/doctor_dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.token,
                    "user_type": this.user_type
                }
            })
            .then(res => {
                const appointments = res.data.appointments || [];
                const appointment = appointments.find(apt => apt.id == this.appointment_id);
                if (appointment) {
                    this.patient_name = appointment.patient_name;
                    this.Department_name = appointment.department_name;
                }
            })
            .catch(err => {
                this.error = err.response?.data?.message || 'Failed to load appointment';
                console.error(this.error);
            });
        }
    }
}
</script>

<style scoped>
.treatment-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #e8d5f8 0%, #c4b5fd 50%, #8b5cf6 100%);
    padding: 2rem;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.page-header {
    margin-bottom: 2.5rem;
    text-align: center;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.page-header h2 {
    color: #581c87;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-header p {
    color: #6b21a8;
    margin: 0.25rem 0 0 0;
    font-size: 1.1rem;
}

.back-btn {
    background: linear-gradient(135deg, #6b7280, #4b5563);
    color: white;
    padding: 0.875rem 1.5rem;
    border-radius: 12px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.back-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(107,114,128,0.4);
    color: white;
}

.patient-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    border: 1px solid rgba(139,92,246,0.2);
    max-width: 500px;
    margin: 0 auto 2rem;
    text-align: center;
}

.patient-avatar {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    color: white;
    font-size: 2rem;
    box-shadow: 0 10px 30px rgba(139,92,246,0.3);
}

.patient-details h4 {
    color: #581c87;
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    font-weight: 700;
}

.department {
    color: #6b21a8;
    margin: 0;
    font-size: 1.1rem;
    background: rgba(139,92,246,0.1);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    display: inline-block;
}

.treatment-form-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 25px 60px rgba(0,0,0,0.15);
    border: 1px solid rgba(139,92,246,0.25);
    max-width: 900px;
    margin: 0 auto;
}

.treatment-form-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #10b981, #059669, #10b981);
    background-size: 200% 100%;
    animation: shimmer 3s ease-in-out infinite;
    border-radius: 24px 24px 0 0;
}

@keyframes shimmer {
    0%, 100% { background-position: 200% 0; }
    50% { background-position: 0 0; }
}

.treatment-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    color: #581c87;
    font-weight: 600;
    margin-bottom: 0.75rem;
    font-size: 1rem;
}

.form-group input,
.form-group select,
.form-group textarea {
    padding: 1.25rem 1.5rem;
    border: 2px solid rgba(139,92,246,0.2);
    border-radius: 16px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.9);
    resize: vertical;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #8b5cf6;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1);
    transform: translateY(-2px);
}

.form-group textarea {
    min-height: 120px;
    font-family: inherit;
}

.form-actions {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    margin-top: 2rem;
}

.btn-submit {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    border: none;
    padding: 1.25rem 3rem;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.4s ease;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    box-shadow: 0 8px 25px rgba(16,185,129,0.3);
}

.btn-submit:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 35px rgba(16,185,129,0.4);
}

.btn-cancel {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    padding: 1.25rem 2.5rem;
    border-radius: 16px;
    text-decoration: none;
    font-weight: 700;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    transition: all 0.4s ease;
    box-shadow: 0 8px 25px rgba(239,68,68,0.3);
}

.btn-cancel:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 35px rgba(239,68,68,0.4);
    color: white;
}

@media (max-width: 768px) {
    .treatment-page {
        padding: 1rem;
    }
    
    .treatment-form-card {
        padding: 2rem 1.5rem;
        margin: 1rem;
    }
    
    .form-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .header-content {
        flex-direction: column;
        text-align: center;
    }
    
    .form-actions {
        flex-direction: column;
    }
    
    .btn-submit,
    .btn-cancel {
        width: 100%;
        justify-content: center;
    }
    
    .patient-card {
        margin: 0 1rem 1.5rem;
        padding: 1.5rem;
    }
}
</style>
