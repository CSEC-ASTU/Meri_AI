
import { CampusNode, RouteEdge } from './types';

export const UNIVERSITY_NAME = "Adama Science and Technology University";
export const APP_NAME = "ASTU Route AI";

// Coordinates centered around ASTU, Adama
// Latitude: 8.5402, Longitude: 39.2693
export const CAMPUS_NODES: CampusNode[] = [
  { id: 'main_gate', name: 'Main Gate', description: 'Primary entrance to the university campus.', category: 'gate', x: 39.2710, y: 8.5420 },
  { id: 'registrar', name: 'Registrar Office', description: 'Administrative block for student records.', category: 'administrative', x: 39.2680, y: 8.5410 },
  { id: 'library', name: 'Main Library', description: 'The central hub for academic research and study.', category: 'academic', x: 39.2695, y: 8.5400 },
  { id: 'block_500', name: 'Block 500', description: 'Engineering and Technology departments.', category: 'academic', x: 39.2660, y: 8.5425 },
  { id: 'block_600', name: 'Block 600', description: 'Applied Sciences and ICT labs.', category: 'academic', x: 39.2720, y: 8.5390 },
  { id: 'cafeteria', name: 'Central Cafeteria', description: 'Main dining hall for students and faculty.', category: 'amenity', x: 39.2685, y: 8.5380 },
  { id: 'stadium', name: 'ASTU Stadium', description: 'Main sports complex and athletic field.', category: 'amenity', x: 39.2730, y: 8.5415 },
  { id: 'dorm_a', name: 'Student Dormitory A', description: 'Residential block for male students.', category: 'residential', x: 39.2650, y: 8.5375 },
  { id: 'admin', name: 'Administrative Building', description: 'President and Vice Presidents offices.', category: 'administrative', x: 39.2700, y: 8.5415 },
];

export const CAMPUS_EDGES: RouteEdge[] = [
  { from: 'main_gate', to: 'admin', weight: 100 },
  { from: 'admin', to: 'registrar', weight: 50 },
  { from: 'registrar', to: 'library', weight: 150 },
  { from: 'library', to: 'block_500', weight: 120 },
  { from: 'library', to: 'block_600', weight: 120 },
  { from: 'block_500', to: 'cafeteria', weight: 100 },
  { from: 'block_600', to: 'cafeteria', weight: 100 },
  { from: 'cafeteria', to: 'dorm_a', weight: 200 },
  { from: 'registrar', to: 'stadium', weight: 250 },
];
