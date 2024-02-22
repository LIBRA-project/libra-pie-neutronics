# LIBRA-pie

## LIBRA-pie basic

This is the basic complete model of LIBRA Pie without added multiplier or reflector with a concrete floor and no walls. 
The P383 neutron generator is also included in this model. This is the model that should be used as a base model for simulations.

## LIBRA-pie 1
This is a model of the LIBRA Pie tank in void without a neutron generator, walls, floor, nor a ceiling.
The script scans through different multiplier types and thicknesses and tallies TBR and neutron current 
through the multiplier. The multiplier is in the shape of a cylindrical quadrant (angle=[0, 90]).

## LIBRA-pie 2
Same as LIBRA-pie 1 except the multiplier is a full cylinder (angle=[0, 360]) and the multiplier has an end cap.

## LIBRA-pie 3
Like LIBRA-pie 1, this model has the LIBRA Pie tank in void without a neutron generator, walls, floor, nor a ceiling.
The script scans through different outer reflector materials and thicknesses and tallies TBR.
The reflector is a sort of cylindrical cap added to the top and sides of the tank.

## LIBRA-pie 4
This model also has the LIBRA Pie tank in void, and has a particular tank reflector like in the LIBRA-pie 3 model.
However, this model scans through generator back reflectors, with a cylindrical shell around the source point behind
the line of sight of the source to the tank, so the back reflector angle goes from 90 to 360 degrees, whereas the tank
is located between 0 to 90 degrees (Quadrant 1). This also tallies TBR.




