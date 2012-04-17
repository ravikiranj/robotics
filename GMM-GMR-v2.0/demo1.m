function demo1
%
% Demo of Gaussian Mixture Regression (GMR). 
% This source code is the implementation of the algorithms described in 
% Section 2.4, p.38 of the book "Robot Programming by Demonstration: A 
% Probabilistic Approach". 
%
% Author:	Sylvain Calinon, 2009
%			http://programming-by-demonstration.org
%
% The program loads a 3D dataset, trains a Gaussian Mixture Model 
% (GMM), and retrieves a generalized version of the dataset with associated 
% constraints through Gaussian Mixture Regression (GMR). Each datapoint 
% has 3 dimensions, consisting of 1 temporal value and 2 spatial values 
% (e.g. drawing on a 2D Cartesian plane). A sequence of temporal values is 
% used as query points to retrieve a sequence of expected spatial 
% distributiuon through Gaussian Mixture Regression (GMR).
%
% This source code is given for free! However, I would be grateful if you refer 
% to the book (or corresponding article) in any academic publication that uses 
% this code or part of it. Here are the corresponding BibTex references: 
%
% @book{Calinon09book,
%   author="S. Calinon",
%   title="Robot Programming by Demonstration: A Probabilistic Approach",
%   publisher="EPFL/CRC Press",
%   year="2009",
%   note="EPFL Press ISBN 978-2-940222-31-5, CRC Press ISBN 978-1-4398-0867-2"
% }
%
% @article{Calinon07,
%   title="On Learning, Representing and Generalizing a Task in a Humanoid Robot",
%   author="S. Calinon and F. Guenter and A. Billard",
%   journal="IEEE Transactions on Systems, Man and Cybernetics, Part B",
%   year="2007",
%   volume="37",
%   number="2",
%   pages="286--298",
% }

%% Definition of the number of components used in GMM.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
nbStates = 4;

%% Load a dataset consisting of 3 demonstrations of a 2D signal.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
load('data/data1.mat'); %load 'Data'
load('data/traj_2_100m_drag.mat'); 
load('data/traj_3_100m_drag.mat'); 
load('data/traj_3_100m_250m_drag.mat'); 
load('data/traj_4_100m_250m_drag.mat');
load('data/traj_4_100m_drag.mat');
load('data/traj_2_250m_drag.mat');
load('data/traj_3_250m_100m_drag.mat');

Data1 = traj_2_100m_drag;
Data2 = traj_3_100m_drag;
Data3 = traj_3_100m_250m_drag;
Data4 = traj_4_100m_250m_drag;
Data5 = traj_4_100m_drag;
Data6 = traj_2_250m_drag;
Data6 = traj_2_250m_drag;
Data7 = traj_3_250m_100m_drag;


% Choose data
Data1 = Data3;
nbVar1 = size(Data1, 1);
Data2 = Data4;
nbVar2 = size(Data2, 1);

%% Training of GMM by EM algorithm, initialized by k-means clustering.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[Priors1, Mu1, Sigma1] = EM_init_kmeans(Data1, nbStates);
[Priors1, Mu1, Sigma1] = EM(Data1, Priors1, Mu1, Sigma1);

[Priors2, Mu2, Sigma2] = EM_init_kmeans(Data2, nbStates);
[Priors2, Mu2, Sigma2] = EM(Data2, Priors2, Mu2, Sigma2);

encodeValue = computeVariation(Priors1, Mu1, Sigma1, Priors2, Mu2, Sigma2);

%% Use of GMR to retrieve a generalized version of the data and associated
%% constraints. A sequence of temporal values is used as input, and the 
%% expected distribution is retrieved. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
expData1(1,:) = linspace(min(Data1(1,:)), max(Data1(1,:)), 100);
[expData1(2:nbVar1,:), expSigma1] = GMR(Priors1, Mu1, Sigma1,  expData1(1,:), [1], [2:nbVar1]);

expData2(1,:) = linspace(min(Data2(1,:)), max(Data2(1,:)), 100);
[expData2(2:nbVar2,:), expSigma2] = GMR(Priors2, Mu2, Sigma2,  expData2(1,:), [1], [2:nbVar2]);

%% Plot of the data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure('position',[10,10,1000,800],'name','GMM-GMR-demo1');
subplot(3, 2, 1); hold on;
plot(Data1(2,:), Data1(3,:), 'x', 'markerSize', 4, 'color', [.3 .3 .3]);
axis([min(Data1(2,:))-0.01 max(Data1(2,:))+0.01 min(Data1(3,:))-0.01 max(Data1(3,:))+0.01]);
xlabel('x','fontsize',16); ylabel('y','fontsize',16);


%% Plot of the GMM encoding results
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subplot(3, 2, 3); hold on;
plotGMM(Mu1([2,3],:), Sigma1([2,3],[2,3],:), [0 .8 0], 1);
axis([min(Data1(2,:))-0.01 max(Data1(2,:))+0.01 min(Data1(3,:))-0.01 max(Data1(3,:))+0.01]);
xlabel('x','fontsize',16); ylabel('y','fontsize',16);

subplot(3, 2, 5); hold on;
plotGMM(expData1([2,3],:), expSigma1([1,2],[1,2],:), [0 0 .8], 2);
axis([min(Data1(2,:))-0.01 max(Data1(2,:))+0.01 min(Data1(3,:))-0.01 max(Data1(3,:))+0.01]);
xlabel('x','fontsize',16); ylabel('y','fontsize',16);

subplot(3, 2, 2); hold on;
plot(Data2(2,:), Data2(3,:), 'x', 'markerSize', 4, 'color', [.3 .3 .3]);
axis([min(Data2(2,:))-0.01 max(Data2(2,:))+0.01 min(Data2(3,:))-0.01 max(Data2(3,:))+0.01]);
xlabel('x','fontsize',16); ylabel('y','fontsize',16);

subplot(3, 2, 4); hold on;
plotGMM(Mu2([2,3],:), Sigma2([2,3],[2,3],:), [0 .8 0], 1);
axis([min(Data2(2,:))-0.01 max(Data2(2,:))+0.01 min(Data2(3,:))-0.01 max(Data2(3,:))+0.01]);
xlabel('x','fontsize',16); ylabel('y','fontsize',16);

subplot(3, 2, 6); hold on;
plotGMM(expData2([2,3],:), expSigma2([1,2],[1,2],:), [0 0 .8], 2);
axis([min(Data2(2,:))-0.01 max(Data2(2,:))+0.01 min(Data2(3,:))-0.01 max(Data2(3,:))+0.01]);
xlabel('x','fontsize',16); ylabel('y','fontsize',16);
encodeString = sprintf('Encode Value = %.2f', encodeValue);
title(encodeString);
