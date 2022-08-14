// Mars lander simulator
// Version 1.11
// Mechanical simulation functions
// Gabor Csanyi and Andrew Gee, August 2019

// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation, to make use of it
// for non-commercial purposes, provided that (a) its original authorship
// is acknowledged and (b) no modified versions of the source code are
// published. Restriction (b) is designed to protect the integrity of the
// exercise for future generations of students. The authors would be happy
// to receive any suggested modifications by private correspondence to
// ahg@eng.cam.ac.uk and gc121@eng.cam.ac.uk.

#include "include/lander.h"
#include <iostream>

double error_term, error_rate, error_int = 0.0, p_out, delta;
vector<float> h_list, v_list, t_list;

void autopilot(void)
// Autopilot to adjust the engine throttle, parachute and attitude control
{

    // standard proportional controller for when the trajectory is already going down
    error_term = -(0.5 + K_h * altitude + velocity * position.norm());
    error_rate = K_h * velocity.y -
                 (acceleration * position.norm() + velocity * velocity.norm());
    error_int = error_int + error_term;
    p_out = K_p * error_term + K_i * error_int + K_d * error_rate;
    delta = (UNLOADED_LANDER_MASS + fuel * FUEL_CAPACITY * FUEL_DENSITY)
        * (GRAVITY * MARS_MASS / position.abs2()) / MAX_THRUST;  // delta = mg, normalised to 0-1

    if (p_out <= -1 * delta) {
        throttle = 0;
    }
    else if (p_out < 1 - delta) {
        throttle = delta + p_out;
    }
    else {
        throttle = 1;
    }

    // deploy the parachute if near the surface, travelling downwards and if it is safe
    if (altitude > 3000 && altitude < 10000 && velocity * position < 0 && safe_to_deploy_parachute()) {
        parachute_status = DEPLOYED;
    }
}

void numerical_dynamics(void)
// This is the function that performs the numerical integration to update the
// lander's pose. The time step is delta_t (global variable).
{

    static vector3d previous_position;
    vector3d new_position;

    lander_mass = (UNLOADED_LANDER_MASS + fuel * FUEL_CAPACITY * FUEL_DENSITY);
    acceleration = thrust_wrt_world() / lander_mass;                                              // thrust
    acceleration -= (GRAVITY * MARS_MASS / position.abs2()) * position.norm();                    // gravity
    acceleration -= 0.5 * DRAG_COEF_LANDER * atmospheric_density(position)                        // atmospheric drag on lander
        * M_PI * LANDER_SIZE * LANDER_SIZE * velocity.abs2() * velocity.norm() / lander_mass;

    if (parachute_status == DEPLOYED)                                                             // parachute drag
        acceleration -= 10 * DRAG_COEF_CHUTE * atmospheric_density(position)
        * LANDER_SIZE * LANDER_SIZE * velocity.abs2() * velocity.norm() / lander_mass;

    // numerical integration: Euler for the first iteration, then Verlet
    /*
    h_list.push_back(altitude);
    v_list.push_back(velocity.abs());
    t_list.push_back(simulation_time); */

    if (simulation_time == 0.0) {
        new_position = position + velocity * delta_t;
        velocity += acceleration * delta_t;
    }
    else {
        new_position = 2 * position - previous_position + delta_t * delta_t * acceleration;
        velocity = (new_position - previous_position) / (2 * delta_t);
    }

    previous_position = position;
    position = new_position;

    //
    //if (altitude < 1) {
    //    // Write the trajectories to file
    //    cout << "Landed or Crashed!" << endl;
    //    ofstream fout;
    //    fout.open("C:\\Users\\lnick\\Documents\\IB Engineering\\Extra Modules\\Mars Lander\\lander_REPO\\lander\\lander\\trajectories_for_scenario_4_with_Kh=" + to_string(K_h) + ".txt");
    //    if (fout) { // file opened successfully
    //        for (int i = 0; i < h_list.size(); i++) {
    //            fout << t_list[i] << ' ' << h_list[i] << endl;
    //        }
    //        exit(0);

    //    }
    //    else { // file did not open successfully
    //        cout << "Could not open trajectory file for writing" << endl;
    //    }
    //}
    //



    // Here we can apply an autopilot to adjust the thrust, parachute and attitude
    if (autopilot_enabled) autopilot();

    // Here we can apply 3-axis stabilization to ensure the base is always pointing downwards
    if (stabilized_attitude) attitude_stabilization();
}

void initialize_simulation(void)
// Lander pose initialization - selects one of 10 possible scenarios
{
    // The parameters to set are:
    // position - in Cartesian planetary coordinate system (m)
    // velocity - in Cartesian planetary coordinate system (m/s)
    // orientation - in lander coordinate system (xyz Euler angles, degrees)
    // delta_t - the simulation time step
    // boolean state variables - parachute_status, stabilized_attitude, autopilot_enabled
    // scenario_description - a descriptive string for the help screen

    scenario_description[0] = "Circular orbit";
    scenario_description[1] = "Descent from 10km";
    scenario_description[2] = "Elliptical orbit";
    scenario_description[3] = "Polar launch at escape velocity, but drag prevents escape";
    scenario_description[4] = "Elliptical orbit with aerobraking";
    scenario_description[5] = "Descent from 200km, exosphere";
    scenario_description[6] = "Areostationary circular orbit";
    scenario_description[7] = "Take-off from Mars surface";
    scenario_description[8] = "Take-off from Phobos, land on Mars";
    scenario_description[9] = "???";

    h_list = {};
    v_list = {};
    t_list = {};

    double error_int = 0.0;

    switch (scenario) {

    case 0:
        // a circular equatorial orbit
        position = vector3d(1.2 * MARS_RADIUS, 0.0, 0.0);
        velocity = vector3d(0.0, -3247.087385863725, 0.0);
        orientation = vector3d(0.0, 90.0, 0.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = false;
        autopilot_enabled = false;
        break;

    case 1:
        // a descent from rest at 10km altitude
        position = vector3d(0.0, -(MARS_RADIUS + 10000.0), 0.0);
        velocity = vector3d(0.0, 0.0, 0.0);
        orientation = vector3d(0.0, 0.0, 90.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = true;
        autopilot_enabled = false;
        break;

    case 2:
        // an elliptical polar orbit
        position = vector3d(0.0, 0.0, 1.2 * MARS_RADIUS);
        velocity = vector3d(3500.0, 0.0, 0.0);
        orientation = vector3d(0.0, 0.0, 90.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = false;
        autopilot_enabled = false;
        break;

    case 3:
        // polar surface launch at escape velocity (but drag prevents escape)
        position = vector3d(0.0, 0.0, MARS_RADIUS + LANDER_SIZE / 2.0);
        velocity = vector3d(0.0, 0.0, 5027.0);
        orientation = vector3d(0.0, 0.0, 0.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = false;
        autopilot_enabled = false;
        break;

    case 4:
        // an elliptical orbit that clips the atmosphere each time round, losing energy
        position = vector3d(0.0, 0.0, MARS_RADIUS + 100000.0);
        velocity = vector3d(4000.0, 0.0, 0.0);
        orientation = vector3d(0.0, 90.0, 0.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = false;
        autopilot_enabled = false;
        break;

    case 5:
        // a descent from rest at the edge of the exosphere
        position = vector3d(0.0, -(MARS_RADIUS + EXOSPHERE), 0.0);
        velocity = vector3d(0.0, 0.0, 0.0);
        orientation = vector3d(0.0, 0.0, 90.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = true;
        autopilot_enabled = false;
        break;

    case 6:
        // areostationary (martian geostationary) circular orbit
        altitude = cbrt(GRAVITY * MARS_MASS / (4 * (M_PI * M_PI) / (MARS_DAY * MARS_DAY))) - MARS_RADIUS;
        position = vector3d(altitude + MARS_RADIUS, 0.0, 0.0);
        velocity = vector3d(0.0, 2 * M_PI / MARS_DAY * (altitude + MARS_RADIUS), 0.0);
        orientation = vector3d(0.0, 90, 0.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = true;
        autopilot_enabled = false;
        break;

    case 7:
        // starting from the martian surface
        position = vector3d(MARS_RADIUS + 10 * LANDER_SIZE / 2, 0.0, 0.0);
        velocity = vector3d(0.0, 0.0, 0.0);
        orientation = vector3d(0.0, 0.07, 0.0);
        delta_t = 0.1;
        parachute_status = NOT_DEPLOYED;
        stabilized_attitude = true;
        autopilot_enabled = false;
        break;

    case 8:
        // starting from the surface of the moon Phobos
        break;

    case 9:
        break;

    }
}

