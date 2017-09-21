# ATL2DSLTrans

Projects with implementation of part of the papers [1,2]. This is a prototype to transform the declarative part of ATL rules to DSLTrans

Usage:

Step 1:
Convert .atl files to .xmi by running ATL2Model
Requires installation of EMFTVM

Step 2:
Run ruleTypeExtraction to obtain *Types.xmi file

Step 3:
Run ATL2DSLTrans with above files to obtain the .dsltrans file

Step 4:
Examine the produced .dsltrans file with the DSLTrans editor in Eclipse (https://github.com/githubbrunob/DSLTransGIT/raw/master/UpdateSiteDSLTrans/site.xml)
Contracts can be created for the transformation with the SyVOLT editor (https://github.com/clagms/SyVOLTEditor/raw/master/SyVoltSyntaxUpdateSite/site.xml)

[1] Bentley James Oakes, Javier Troya, Levi Lucio, Manuel Wimmer. "Fully Verifying Transformation Contracts for Declarative ATL". Proceedings of the ACM/IEEE 18th International Conference on Model Driven Engineering Languages and Systems (MoDELS 2015). Ottawa, Ontario, Canada. September 30 - October 2

[2] Bentley James Oakes, Javier Troya, Levi Lúcio, Manuel Wimmer. "Full contract verification for ATL using symbolic execution". Software and Systems Modeling (2016), pp. 1--35
