import uuid
from requests import get as api_get_request
from methods.shared import common
from utils.prescription_id_generator import get_new_prescription_id


def prepare_new_prescription_body(**kwargs):
    bundle_id = uuid.uuid4()
    message_header_id = uuid.uuid4()
    data = {
        "resourceType": "Bundle",
        "id": bundle_id,
        "identifier": {
            "system": "https://tools.ietf.org/html/rfc4122",
            "value": uuid.uuid4()
        },
        "type": "message",
        "entry": [
            {
                "fullUrl": f"urn:uuid:{bundle_id}",
                "resource": {
                    "resourceType": "MessageHeader",
                    "id": message_header_id,
                    "eventCoding": {
                        "system": "https://fhir.nhs.uk/CodeSystem/message-event",
                        "code": "prescription-order",
                        "display": "Prescription Order"
                    },
                    "sender": {
                        "identifier": {
                            "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                            "value": "RBA"
                        },
                        "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
                        "display": "RAZIA|ALI"
                    },
                    "source": {
                        "endpoint": "urn:nhs-uk:addressing:ods:RBA"
                    },
                    "destination": [
                        {
                            "endpoint": "urn:nhs-uk:addressing:ods:RX801",
                            "receiver": {
                                "identifier": {
                                    "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                    "value": "RX801"
                                }
                            }
                        }
                    ],
                    "focus": [
                        {
                            "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
                        },
                        {
                            "reference": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6"
                        }
                    ]
                }
            },
            {
                "fullUrl": "urn:uuid:a54219b8-f741-4c47-b662-e4f8dfa49ab6",
                "resource": {
                    "resourceType": "MedicationRequest",
                    "id": "a54219b8-f741-4c47-b662-e4f8dfa49ab6",
                    "extension": [
                        {
                            "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionType",
                            "valueCoding": {
                                "system": "https://fhir.nhs.uk/CodeSystem/prescription-type",
                                "code": "1001",
                                "display": "Outpatient Community Prescriber - Medical Prescriber"
                            }
                        }
                    ],
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/prescription-order-item-number",
                            "value": "{{order_item_1_number}}"
                        }
                    ],
                    "status": "active",
                    "intent": "order",
                    "category": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
                                    "code": "outpatient",
                                    "display": "Outpatient"
                                }
                            ]
                        }
                    ],
                    "medicationCodeableConcept": {
                        "coding": [
                            {
                                "system": "http://snomed.info/sct",
                                "code": "15517911000001104",
                                "display": "Methotrexate 10mg/0.2ml solution for injection pre-filled syringes"
                            }
                        ]
                    },
                    "subject": {
                        "reference": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2"
                    },
                    "authoredOn": "2023-09-22T14:47:29+00:00",
                    "requester": {
                        "reference": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666"
                    },
                    "groupIdentifier": {
                        "extension": [
                            {
                                "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PrescriptionId",
                                "valueIdentifier": {
                                    "system": "https://fhir.nhs.uk/Id/prescription",
                                    "value": "1dfb1898-70dd-42df-ace4-aa0fd83a501a"
                                }
                            }
                        ],
                        "system": "https://fhir.nhs.uk/Id/prescription-order-number",
                        "value": "{{prescription_id}}"
                    },
                    "courseOfTherapyType": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-course-of-therapy",
                                "code": "acute",
                                "display": "Short course (acute) therapy"
                            }
                        ]
                    },
                    "dosageInstruction": [
                        {
                            "text": "Inject 10 milligram - 5 times a day - Subcutaneous route - for 10 days",
                            "timing": {
                                "repeat": {
                                    "frequency": 5,
                                    "period": 1,
                                    "periodUnit": "d",
                                    "boundsDuration": {
                                        "value": 10,
                                        "unit": "day",
                                        "system": "http://unitsofmeasure.org",
                                        "code": "d"
                                    }
                                }
                            },
                            "method": {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "422145002",
                                        "display": "Inject"
                                    }
                                ]
                            },
                            "route": {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "34206005",
                                        "display": "Subcutaneous route"
                                    }
                                ]
                            },
                            "doseAndRate": [
                                {
                                    "doseQuantity": {
                                        "value": 10,
                                        "unit": "milligram",
                                        "system": "http://unitsofmeasure.org",
                                        "code": "mg"
                                    }
                                }
                            ]
                        }
                    ],
                    "dispenseRequest": {
                        "extension": [
                            {
                                "url": "https://fhir.nhs.uk/StructureDefinition/Extension-DM-PerformerSiteType",
                                "valueCoding": {
                                    "system": "https://fhir.nhs.uk/CodeSystem/dispensing-site-preference",
                                    "code": "P1"
                                }
                            }
                        ],
                        "quantity": {
                            "value": 1,
                            "unit": "pre-filled disposable injection",
                            "system": "http://snomed.info/sct",
                            "code": "3318611000001103"
                        },

                        "performer": {
                            "identifier": {
                                "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                "value": get_new_prescription_id()
                            }
                        }
                    },
                    "substitution": {
                        "allowedBoolean": False
                    }
                }
            },
            {
                "fullUrl": "urn:uuid:78d3c2eb-009e-4ec8-a358-b042954aa9b2",
                "resource": {
                    "resourceType": "Patient",
                    "id": "78d3c2eb-009e-4ec8-a358-b042954aa9b2",
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/nhs-number",
                            "value": "{{nhs_number}}"
                        }
                    ],
                    "name": [
                        {
                            "use": "usual",
                            "family": "CORY",
                            "given": [
                                "ETTA"
                            ],
                            "prefix": [
                                "MISS"
                            ]
                        }
                    ],
                    "gender": "female",
                    "birthDate": "1999-01-04",
                    "address": [
                        {
                            "use": "home",
                            "line": [
                                "123 Dale Avenue",
                                "Long Eaton",
                                "Nottingham"
                            ],
                            "postalCode": "NG10 1NP"
                        }
                    ],
                    "generalPractitioner": [
                        {
                            "identifier": {
                                "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                "value": "B81001"
                            }
                        }
                    ]
                }
            },
            {
                "fullUrl": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a",
                "resource": {
                    "resourceType": "Practitioner",
                    "id": "a8c85454-f8cb-498d-9629-78e2cb5fa47a",
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/sds-user-id",
                            "value": "{{user_id}}"
                        },
                        {
                            "system": "https://fhir.hl7.org.uk/Id/nmc-number",
                            "value": "12A3456B"
                        }
                    ],
                    "name": [
                        {
                            "family": "Userq",
                            "given": [
                                "Random"
                            ],
                            "prefix": [
                                "MR"
                            ]
                        }
                    ]
                }
            },
            {
                "fullUrl": "urn:uuid:56166769-c1c4-4d07-afa8-132b5dfca666",
                "resource": {
                    "resourceType": "PractitionerRole",
                    "id": "56166769-c1c4-4d07-afa8-132b5dfca666",
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/sds-role-profile-id",
                            "value": "100102238986"
                        },
                        {
                            "system": "https://fhir.hl7.org.uk/Id/nhsbsa-spurious-code",
                            "value": "12A3456B"
                        }
                    ],
                    "practitioner": {
                        "reference": "urn:uuid:a8c85454-f8cb-498d-9629-78e2cb5fa47a"
                    },
                    "organization": {
                        "reference": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8"
                    },
                    "code": [
                        {
                            "coding": [
                                {
                                    "system": "https://fhir.nhs.uk/CodeSystem/NHSDigital-SDS-JobRoleCode",
                                    "code": "S8001:G8001:R8001",
                                    "display": "Nurse Access Role"
                                }
                            ]
                        }
                    ],
                    "telecom": [
                        {
                            "system": "phone",
                            "value": "01234567890",
                            "use": "work"
                        }
                    ]
                }
            },
            {
                "fullUrl": "urn:uuid:3b4b03a5-52ba-4ba6-9b82-70350aa109d8",
                "resource": {
                    "resourceType": "Organization",
                    "id": "3b4b03a5-52ba-4ba6-9b82-70350aa109d8",
                    "identifier": [
                        {
                            "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                            "value": "A99968"
                        }
                    ],
                    "name": "SOMERSET BOWEL CANCER SCREENING CENTRE",
                    "address": [
                        {
                            "use": "work",
                            "line": [
                                "MUSGROVE PARK HOSPITAL"
                            ],
                            "city": "TAUNTON",
                            "postalCode": "TA1 5DA"
                        }
                    ],
                    "telecom": [
                        {
                            "system": "phone",
                            "value": "01823 333444",
                            "use": "work"
                        }
                    ],
                    "partOf": {
                        "identifier": {
                            "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                            "value": "RBA"
                        },
                        "display": "TAUNTON AND SOMERSET NHS FOUNDATION TRUST"
                    }
                }
            }
        ]
    }

