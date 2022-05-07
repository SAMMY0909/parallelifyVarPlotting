#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##globalplotvar.py
import numpy as np
from h5py import File

Bins = {
  "numberOfInnermostPixelLayerHits" : np.arange(5),
  "numberOfNextToInnermostPixelLayerHits": np.arange(5),
  "numberOfInnermostPixelLayerSharedHits": np.arange(5),
  "numberOfInnermostPixelLayerSplitHits" : np.arange(5),
  "numberOfPixelHits" : np.arange(10),
  "numberOfPixelHoles": np.arange(10),
  "numberOfPixelSharedHits" : np.arange(10),
  "numberOfPixelSplitHits"  : np.arange(10),
  "numberOfSCTHits" : np.arange(30),
  "numberOfSCTHoles": np.arange(30),
  "numberOfSCTSharedHits" : np.arange(30),
  "expectNextToInnermostPixelLayerHit" : np.arange(5),
  "expectInnermostPixelLayerHit" : np.arange(5),
  "radiusOfFirstHit" : np.arange(0, 150, 10),
  "chiSquared" : np.arange(0, 50, 5),
  "numberDoF" : np.arange(0, 50, 5),
  "ptfrac": np.arange(0, 1, 10),
  "pt"  : np.arange(0, 10000, 500),
  "eta" : np.arange(-3, 3, 0.1),
  "deta" : np.arange(0, 6, 0.1),
  "dphi" : np.arange(0, 5, 0.1),
  "theta" : np.arange(0, 5, 0.1),
  "dr" : np.arange(0, 5, 0.1),
  "qOverP" : np.arange(0, 0.001, 0.0001),
  "qOverPUncertainty" : np.arange(0, 0.001, 0.0001),
  "phiUncertainty" : np.arange(0, 5, 0.1),
  "thetaUncertainty" : np.arange(0, 5, 0.1),
  "IP3D_signed_d0" : np.arange(-10, 10, 1),
  "IP2D_signed_d0" : np.arange(-10, 10, 1),
  "IP3D_signed_z0" : np.arange(-30, 30, 1),
  "d0" : np.arange(-10, 10, 1),
  "z0SinTheta" : np.arange(-30, 30, 1),
  "d0Uncertainty" : np.arange(-1, 1, 0.1),
  "z0SinThetaUncertainty" :  np.arange(-3, 3, 0.1),
  "IP3D_signed_d0_significance" : np.arange(-30, 30, 1),
  "IP3D_signed_z0_significance" : np.arange(-50, 50, 1),
  "z0RelativeToBeamspot": np.arange(-50, 50, 1),
  "z0RelativeToBeamspotUncertainty" : np.arange(-5, 5, 0.1),
}

variables = {
    "hits": [
        "numberOfInnermostPixelLayerHits",
        "numberOfNextToInnermostPixelLayerHits",
        "numberOfInnermostPixelLayerSharedHits",
        "numberOfInnermostPixelLayerSplitHits",
        "numberOfPixelHits",
        "numberOfPixelHoles",
        "numberOfPixelSharedHits",
        "numberOfPixelSplitHits",
        "numberOfSCTHits",
        "numberOfSCTHoles",
        "numberOfSCTSharedHits",
        "expectNextToInnermostPixelLayerHit",
        "expectInnermostPixelLayerHit",
        "radiusOfFirstHit",
    ],
    "quality": [
        "chiSquared",
        "numberDoF",
        "ptfrac",
    ],
    "kine": [
        "pt",
        "eta",
        "deta",
        "dphi",
        "theta",
        "dr",
        "qOverP",
        "qOverPUncertainty",
        "phiUncertainty",
        "thetaUncertainty",
    ], 
    "ips": [
        "IP3D_signed_d0",
        "IP2D_signed_d0",
        "IP3D_signed_z0",
        "d0",
        "z0SinTheta",
        "d0Uncertainty",
        "z0SinThetaUncertainty",
        "IP3D_signed_d0_significance",
        "IP3D_signed_z0_significance",
        "z0RelativeToBeamspot",
        "z0RelativeToBeamspotUncertainty"
    ], 
}

def tracksel(input_file ,flavor:int) :
    flavor=int(flavor) #LOL, just making sure
    with File(input_file, 'r') as h5file:
        tracks = h5file['tracks_from_jet']
        jets = h5file['jets'][0:670000]
        flavjets = (jets["HadronConeExclTruthLabelID"] == flavor).nonzero()[0]
        flav_tracks= tracks[flavjets,:]
        rownum,colnum=flav_tracks.shape
        print(f"The dimensions of the selected tracks corresponding to jet flavor {flavor} in file {input_file} is: " +str(rownum)+" by "+str(colnum))
        for vartype in variables:
            for var in variables[vartype]:
                sel_flav_tracks = flav_tracks[flav_tracks["valid"] == 1]
        
        return sel_flav_tracks
