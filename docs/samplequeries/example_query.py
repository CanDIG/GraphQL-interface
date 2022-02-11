long_query = """ 
query beaconQuery($rName: String!, $rBase: String!, $aBase: String!, $start: Int!, $end: Int!)
{
  beaconQuery(
    input: {
      referenceName: $rName
      referenceBases: $rBase
      alternateBases: $aBase
      start: $start
      end: $end
    }
  ) {
    exists
    error {
      errorCode
      errorMessage
    }
    alleleRequest {
      referenceName
      referenceBases
      start
      end
      alternateBases
      datasetIds
    }
    individualsPresent {
      personalInfo {
        ...subjectFields
      }
      mcodepackets {
        ...mCODEFields
      }
      phenopackets {
        ...phenopacketFields
      }
    }
    beaconId
    apiVersion
  }
}

fragment phenotypicFields on PhenotypicFeature {
  id
  description
  type {
    id
  }
  negated
  severity {
    id
  }
  onset {
    id
  }
  modifier {
    id
  }
  evidence {
    id
  }
  biosample
  extraProperties
  created
  updated
}

fragment biosampleFields on Biosample {
  id
  phenotypicFeatures {
    ...phenotypicFields
  }
  individual
  description
  sampledTissue {
    reference
    display
    id
    label
  }
  taxonomy {
    label
  }
  histologicalDiagnosis {
    label
  }
  tumorProgression {
    label
  }
  tumorGrade {
    label
  }
  diagnosticMarkers {
    label
  }
  procedure {
    code {
      label
    }
    bodySite {
      label
    }
    extraProperties
  }
  htsFiles
  variants {
    id
    alleleType
    allele {
      id
    }
    zygosity {
      id
    }
    extraProperties
    hgvsAllele
  }
  isControlSample
  extraProperties
  created
  updated
}

fragment subjectFields on Individual {
  id
  alternateIds
  dateOfBirth
  sex
  karyotypicSex
  taxonomy {
    id
  }
  active
  deceased
  comorbidCondition {
    code {
      label
    }
    clinicalStatus {
      label
    }
  }
  ecogPerformanceStatus {
    label
  }
  karnofsky {
    label
  }
  race
  ethnicity
  extraProperties
  created
  updated
  phenopackets
  biosamples {
    ...biosampleFields
  }
}

fragment mCODEFields on MCodePacket {
  id
  subject {
    ...subjectFields
  }
  genomicsReport {
    code {
      label
    }
    performingOrganizationName
    issued
    geneticSpecimen {
      id
      specimenType {
        label
      }
      collectionBody {
        label
      }
      laterality {
        label
      }
      extraProperties
    }
    geneticVariant {
      id
      dataValue {
        label
      }
      method {
        label
      }
      aminoAcidChange {
        label
      }
      aminoAcidChangeType {
        label
      }
      cytogeneticLocation {
        label
      }
      cytogeneticNomenclature {
        label
      }
      geneStudied {
        id
        alternateIds
        symbol
        extraProperties
      }
      genomicDnaChange {
        label
      }
      genomicSourceClass {
        label
      }
      variationCode {
        label
      }
      extraProperties
    }
    genomicRegionStudied {
      id
      dnaRangesExamined {
        label
      }
      dnaRegionDescription
      geneMutation {
        label
      }
      geneStudied {
        label
      }
      genomicReferenceSequenceId
      genomicRegionCoordinateSystem {
        label
      }
      extraProperties
    }
    extraProperties
  }
  cancerCondition {
    tnmStaging {
      tnmType
      stageGroup {
        dataValue {
          label
        }
      }
      primaryTumorCategory {
        dataValue {
          label
        }
      }
      regionalNodesCategory {
        dataValue {
          label
        }
      }
      distantMetastasesCategory {
        dataValue {
          label
        }
      }
      extraProperties
      cancerCondition
    }
    conditionType
    bodySite {
      label
    }
    laterality {
      label
    }
    clinicalStatus {
      label
    }
    code {
      label
    }
    dateOfDiagnosis
    histologyMorphologyBehavior {
      label
    }
    verificationStatus {
      label
    }
    extraProperties
  }
  medicationStatement {
    medicationCode {
      label
    }
    terminationReason {
      label
    }
    treatmentIntent {
      label
    }
    startDate
    endDate
    extraProperties
  }
  dateOfDeath
  cancerDiseaseStatus {
    label
  }
  cancerRelatedProcedures {
    id
    procedureType
    code {
      label
    }
    bodySite {
      label
    }
    laterality {
      label
    }
    treatmentIntent {
      label
    }
    reasonCode {
      label
    }
    reasonReference
    extraProperties
  }
  table
  extraProperties
}

fragment phenopacketFields on Phenopacket {
  id
  subject {
    ...subjectFields
  }
  phenotypicFeatures {
    ...phenotypicFields
  }
  biosamples {
    ...biosampleFields
  }
  genes {
    id
    alternateIds
    symbol
    created
    updated
    extraProperties
  }
  variants {
    id
    allele {
      id
    }
    alleleType
    hgvsAllele
    zygosity {
      id
    }
    extraProperties
  }
  diseases {
    id
    term {
      label
    }
    diseaseStage {
      label
    }
    tnmFinding {
      label
    }
    extraProperties
  }
  htsFiles {
    uri
    description
    htsFormat
    genomeAssembly
    individualToSampleIdentifiers
    extraProperties
  }
  metaData {
    id
    created
    createdBy
    submittedBy
    resources {
      id
      name
      namespacePrefix
      url
      version
      iriPrefix
      extraProperties
    }
    updates {
      timestamp
      updatedBy
      comment
    }
    phenopacketSchemaVersion
    externalReferences {
      id
      description
    }
    extraProperties
  }
}
"""