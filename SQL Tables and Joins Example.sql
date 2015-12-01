use BuildingEnergy;

# creating the first two tables and adding the initial values

CREATE TABLE EnergyCategories(
energycategory VARCHAR(25),
cat_ID INT(1));

CREATE TABLE EnergyTypes(
energytype VARCHAR(25),
type_ID INT(1));

INSERT INTO EnergyTypes(energytype, type_ID)

VALUES

('Electricity',1),('Fuel Oil',2),('Gas',3),('Solar',4),('Steam',5),('Wind',6);

INSERT INTO EnergyCategories(energycategory, cat_ID)

VALUES

('Fossil',1),('Fossil',2),('Fossil',3),('Renewable',4),('Fossil',5),('Renewable',6);

# running a test join to see that fossils and renewables are paired to the correct type

SELECT EnergyCategories.energycategory, EnergyTypes.energytype
FROM EnergyCategories
JOIN EnergyTypes
ON EnergyCategories.cat_ID = EnergyTypes.type_ID;

# create the buildings table and insert the values

CREATE TABLE Buildings
(
building VARCHAR(40),
build_id INT(1)
);

INSERT INTO Buildings(building, build_ID)
VALUES
('Borough of Manhattan Community College', 1),('Chrysler Building', 2),('Empire State Building',3);

# create the bridge table for EnergyTypes and Buildings and insert the relations

CREATE TABLE build_types
(
type_ID INT NOT NULL REFERENCES EnergyTypes(type_ID),
build_ID INT NOT NULL REFERENCES Buildings(build_ID)
);

INSERT INTO build_types(build_ID,type_ID)
VALUES
(1,1),(1,4),(1,5),(2,1),(2,5),(3,1),(3,3),(3,5);

# join that shows each building and each type that building uses

SELECT B.building, E.energytype
FROM Buildings b
INNER JOIN build_types bt ON B.build_ID = bt.build_ID
INNER JOIN EnergyTypes e ON bt.type_ID = E.type_ID
ORDER BY B.building;

# new additions to the buildings and energy types table, and corresponding relations

INSERT INTO Buildings(building,build_ID)
VALUES
('Bronx Lions House', 4),('Brooklyn Childrens Museum',5);

INSERT INTO EnergyTypes(energytype,type_ID)
VALUES
('Geothermal',7);

INSERT INTO build_types(build_id,type_ID)
VALUES
(4,7),(5,1),(5,7);

INSERT INTO EnergyCategories(energycategory,cat_ID)
VALUES
('Renewable',7);

# query that will display only buildings with renewable energy, and their energy type.

SELECT B.building, T.energytype, C.energycategory
FROM Buildings b
INNER JOIN build_types bt ON B.build_ID = bt.build_ID
INNER JOIN EnergyTypes T ON bt.type_ID = T.type_ID
INNER JOIN EnergyCategories C ON C.cat_ID = T.type_ID
WHERE C.energycategory = 'Renewable';

# Counts the number of each energy type that appears for each building

SELECT E.energytype, COUNT(*)
FROM Buildings b
LEFT JOIN build_types bt ON B.build_ID = bt.build_ID
LEFT JOIN EnergyTypes e ON bt.type_ID = E.type_ID
GROUP BY E.energytype;

SELECT * FROM EnergyCategories;
SELECT * FROM EnergyTypes;
SELECT * FROM Buildings;
SELECT * FROM build_types;

DROP TABLE EnergyCategories;
DROP TABLE EnergyTypes;
DROP TABLE Buildings;
DROP TABLE build_types;