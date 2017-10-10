package ruleTypeExtraction;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import org.eclipse.core.runtime.NullProgressMonitor;
import org.eclipse.m2m.atl.common.ATLExecutionException;
import org.eclipse.m2m.atl.core.ATLCoreException;

import ruleTypeExtraction.files.*;

public class Standalone {

	public static void main(String[] args) {
		String pathSrcEcoreMMFile = args[0];
		String pathTrgEcoreMMFile = args[1];
		String pathATLTransformation = args[2];
		String pathOUTFile = args[3];
		String pathOUTFileSuffix = "";
		
		if (args.length == 5)
			pathOUTFileSuffix = args[4];
		
		String[] s = pathATLTransformation.split("/");
		String ATLTransName = s[s.length-1];
		
		ATLFile2Model afm = new ATLFile2Model(pathATLTransformation, "tempModel.xmi");
		try{
			//messageLabel.setText(afm.injectATLTrafo());
			afm.injectATLTrafo();
			System.out.println("Textual ATL transformation injected into a model --> OK \n --- \n");
			System.out.println("Extracting types from model (this may take some time depending on the size of the model transformation)...... \n");
		} catch (FileNotFoundException e){
			
			System.out.println("FileNotFoundException: " + e.toString());
			
			e.printStackTrace();
			return;
			
		} catch (ATLCoreException e){
			
			System.out.println("ATLCoreException: " + e.toString());
			
			e.printStackTrace();
			return;
		}
		try {
			ExtractRuleTypes runner = new ExtractRuleTypes();
			runner.loadModels("tempModel.xmi", "file:/"+pathSrcEcoreMMFile, "file:/"+pathTrgEcoreMMFile);
			runner.doExtractRuleTypes(new NullProgressMonitor());
			runner.saveModels("tempTypesExtracted.xmi");
			
			//runner.saveModels(pathOUTFile + "/" + 
				//	ATLTransName.substring(0, ATLTransName.lastIndexOf('.')) + "Types.xmi");
			System.out.println(" --- \n Types extracted from model --> OK \n");
			
		
			/*SimilarityMatrix sm = new SimilarityMatrix("tempTypesExtracted.xmi", pathOUTFile + "/" + 
								ATLTransName.substring(0, ATLTransName.lastIndexOf('.')) + "SM.csv");
			sm.main();
			messageLabel.append(" --- \n File with Similarity Matrix created --> OK \n");
			messageLabel.update(messageLabel.getGraphics());*/
			
			File f = new File("tempTypesExtracted.xmi"); // This file contains the model with the types extracted
			File fl = new File (pathOUTFile + "/" +      // We want to copy the model before into this one
					ATLTransName.substring(0, ATLTransName.lastIndexOf('.')) + "Types" + pathOUTFileSuffix + ".xmi");
						
			InputStream input = null;
			OutputStream output = null;
			try {
			 input = new FileInputStream(f);
			 output = new FileOutputStream(fl);
			 byte[] buf = new byte[1024];
			 int bytesRead;
			 while ((bytesRead = input.read(buf)) > 0) {
			         output.write(buf, 0, bytesRead);
			 }
			 input.close();
			 output.close();
			 f.delete();

			 //Deleting temporal files:
			 File tmp2 = new File("tempModel.xmi");
			 tmp2.delete();
			 
			}catch (FileNotFoundException e){
				
				System.out.println("FileNotFoundException: " + e.toString());
				
				e.printStackTrace();
			} catch (IOException e){
				
				System.out.println("IOException: " + e.toString());
				
				e.printStackTrace();
			}
		
		} catch (ATLCoreException e) {
			
			System.out.println("ATLCoreException: " + e.toString());
			
			e.printStackTrace();
			return;
		} catch (IOException e) {
			
			System.out.println("IOException: " + e.toString());
			
			e.printStackTrace();
			return;
		} catch (ATLExecutionException e) {
			
			System.out.println("ATLExecutionException: " + e.toString());
			
			e.printStackTrace();
			return;
		}
	}

}
