function val = computeVariation(Priors1, Mu1, Sigma1, Priors2, Mu2, Sigma2);
    diffSigma = abs(Sigma1 - Sigma2);
    temp = sum(diffSigma, 2);
    sigmaVariation = sum(temp, 3);
    muVariation = sum(abs(Mu1-Mu2), 2);    
    totalVariation = sigmaVariation + muVariation;
    val = sum(totalVariation);    
end

