FROM Patient AS A
LEFT OUTER JOIN StudyInformation AS B ON A.PatientID = B.PatientID
LEFT OUTER JOIN History AS C ON A.PatientID = C.PatientID
LEFT OUTER JOIN IPRanges ON C.ChangeDate BETWEEN IPRanges.StartTime AND IPRanges.EndTime