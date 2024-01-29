# Contains conventions for stuff and things


# Unit abbreviations
NOTE: ALL variables that have units should have them noted in their names  

use _ to denote "per" or division of units  
ie momentum uses kgm_s (kilogram-meters-per-second)  

use numbers after a unit to denote exponents  
ie acceleration uses m_s2  

avoid using negative exponents as - is not allowed in variable names  
    just rewrite it with positive exponents (ms-2 doesn't work so use m_s2)  

if units are ever confusing make note of them in the code and add a comment `#UNITS` near the variable definition

| unit name | abbreviation |
| - | - | - |
| seconds | s |
| samples | smp |
| Hertz | Hz |
