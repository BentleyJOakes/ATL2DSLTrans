# ATL2DSLTrans

Project to automate the conversion of the ATL Zoo from ATL to DSLTrans. Note that we convert the the declarative part of ATL rules to DSLTrans. For further information, see [1,2].

 Note that not all examples may be successfully transformed at this time.


Usage:
In the convertor folder, 'python zoo_to_dsltrans.py'.
This will download, extract, and attempt to automate the following steps.

Step 1:
Convert .atl files to .xmi by running the ATL2Model launch configurations
Requires installation of EMFTVM in Eclipse

Step 2:
Run ruleTypeExtraction to obtain *Types.xmi file

Step 3:
Run ATL2DSLTrans project with above files to obtain the .dsltrans file

Step 4:
Examine the produced .dsltrans file with the DSLTrans editor in Eclipse (https://github.com/githubbrunob/DSLTransGIT/raw/master/UpdateSiteDSLTrans/site.xml)
Contracts can be created for the transformation with the SyVOLT editor (https://github.com/clagms/SyVOLTEditor/raw/master/SyVoltSyntaxUpdateSite/site.xml)

[1] Bentley James Oakes, Javier Troya, Levi Lucio, Manuel Wimmer. "Fully Verifying Transformation Contracts for Declarative ATL". Proceedings of the ACM/IEEE 18th International Conference on Model Driven Engineering Languages and Systems (MoDELS 2015). Ottawa, Ontario, Canada. September 30 - October 2

[2] Bentley James Oakes, Javier Troya, Levi Lúcio, Manuel Wimmer. "Full contract verification for ATL using symbolic execution". Software and Systems Modeling (2016), pp. 1--35
