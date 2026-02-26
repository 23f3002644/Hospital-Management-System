import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import Patient_dash from '@/pages/Patients/Patient_dash.vue'
import Doctor_dash from '@/pages/Doctors/Doctor_dash.vue'
import Dashboard from '@/pages/AdminPages/Dashboard.vue'
import Department_details from '@/pages/Patients/Department_details.vue'
import Doctor_details from '@/pages/Patients/Doctor_details.vue'
import Appointment from '@/pages/Patients/Appointment.vue'
import History from '@/pages/Patients/History.vue'
import Update from '@/pages/Patients/Update.vue'
import Treatment from '@/pages/Doctors/Treatment.vue'
import Upcoming_Appointments from '@/pages/AdminPages/Upcoming_Appointments.vue'
import Patients from '@/pages/AdminPages/Patients.vue'
import Doctors from '@/pages/AdminPages/Doctors.vue'
import Add_doctor from '@/pages/AdminPages/Add_doctor.vue'
import Edit_doctor from '@/pages/AdminPages/Edit_doctor.vue'
import All_treatment from '@/pages/AdminPages/All_treatment.vue'
import Search from '@/pages/Patients/Search.vue'
import Departments from '@/pages/AdminPages/Departments.vue'
import Add_department from '@/pages/AdminPages/Add_department.vue'
import Availabilty_slot from '@/pages/Doctors/Availabilty_slot.vue'


const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/patient_dash', name: 'Patient_dash', component: Patient_dash },
  { path: '/doctor_dash', name: 'Doctor_dash', component: Doctor_dash },
  {path: '/dashboard', name: 'Dashboard', component: Dashboard},
  {path: '/department_details/:id', name: 'Department_details',component:Department_details},
  {path: '/doctor_details/:id', name: 'Doctor_details', component: Doctor_details},
  {path: '/appointment/:department/:doctor_id', name: 'Appointment', component: Appointment},
  {path: '/patient/history/:id', name: 'Patient_history', component: History},
  {path: '/patient/update/:id', name: 'Update_patient', component: Update},
  {path: '/treatment/:id', name: 'Treatment', component: Treatment},
  {path: '/upcoming_appointments', name: 'Upcoming_appointments', component: Upcoming_Appointments},
  {path: '/registered_patients', name: 'Registered_patients', component: Patients},
  {path: '/registered_doctors', name: 'Registered_doctors', component: Doctors},
  {path: '/add_doctor', name: 'Add_doctor', component: Add_doctor},
  {path: '/edit_doctor/:id', name: 'Edit_doctor', component: Edit_doctor},
  {path: '/all_treatments', name: 'All_treatments', component: All_treatment },
  {path: '/search_doctor', name: 'Search_doctor', component: Search},
  {path: '/all_departments', name: 'All_departments', component: Departments},
  {path: '/add_department', name: 'Add_department', component: Add_department},
  {path: '/availability_slot/:doctor_id', name: 'Availability_slot', component: Availabilty_slot},
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes  // --> routes: routes
})

export default router
