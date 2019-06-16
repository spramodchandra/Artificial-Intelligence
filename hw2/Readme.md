## Problem Description
Los Angeles Homeless Services Authority (LAHSA) and Safe Parking LA (SPLA) are two organizations in Los Angeles that service the homeless community. LAHSA provides beds in shelters and SPLA manages spaces in parking lots for people living in their cars. In the city’s new app for homelessness, people in need of housing can apply for a space with either service. For this homework, you will help SPLA choose applicants that meet the SPLA specific requirements for the space and that also optimize the use of the parking lot for that week.

## Approach
Traditional Game playing approaches like min-max can't be used as this is not a zero sum game.
So the approach implemented uses DFS to explore multiple paths, using many heuristics to prune paths, using some optimisations techniques in terms as single player game playing, hash to reduces the branches etc. Based on problem description mentioned in the pdf, a non cooperative approach has been used to maximize the utilization of parking lot for that week.
