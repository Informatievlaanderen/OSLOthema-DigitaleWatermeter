# OSLOthema - configuration files

This branch should be used to manage the configuration files of the OSLOthema repositories. The configuration files are used to validatate the OSLOthema configuration files in each thema-repository. These files shouldn't be touched by the editors of OSLO

## /types

This directory contains the different typescript configuration files. The configuration files are used to generate the JSON schema files in the `/schemas` directory.

## /schemas

This directory contains the different JSON schema files. These files are generated using the TypeScript files defined in `/types`. The schema files are used to validate the OSLOthema configuration files in each thema-repository.
