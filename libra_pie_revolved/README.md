#LIBRA-pie-revolved

## Basic Model
This is the base model of the four quadrants of the LIBRA-pie tank to make the full LIBRA experiment,
with the neutron generator, multiplier, and concrete floor. It includes 3 thermocouple tubes, 2 gas tubes,
1 fill tube, and 3 re-entrant heater tubes in addition to a center tank with a heater re-entrant tube.

## Height Scan
Model of LIBRA based off of the LIBRA-pie tank design, and is the same as the basic model, except there are no tubes
nor re-entrant tubes. The model tallies the TBR and scans through various salt heights, but changes the outer radius 
of the salt to keep the salt volume constant. Uses lead and borated-polyethylene shielding on the outside.

## Mult-Thickness-Scan
Similar to height scan, the LIBRA experiment is modeled off of the LIBRA-pie tank design without any tubing, but 
the inner radius of the tank is varied as multiplier is added, while the outer radius and height of salt remain constant.
Uses lead and borated-polyethylene shielding on the outside.

## Reflector-Scan
Model of LIBRA experiment similar to height and mult-thickness scans, but does not have the lead and borated-polyethylene shielding.
The script scans through various outer tank reflector materials and thicknesses for a given salt height, and tank inner radius, 
and multiplier thickness.

## Reflector-Scan-2
Same as the Reflector-Scan, but only uses graphite reflector and uses the Basic Model salt height, inner radius, and multiplier thickness.
The script also models two-component reflectors.

## Size-Scan
Based on the LIBRA-pie revolved Basic Model, this script scans through various salt heights and thicknesses by changing the tank cover z-point
and the tank outer radius, while keeping the inner radius the same as in the Basic Model. The script also creates a contour map of the TBRs at
various salt thicknesses and heights.