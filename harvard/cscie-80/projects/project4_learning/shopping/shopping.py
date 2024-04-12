import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - 1 Administrative, an integer
        - 2 Administrative_Duration, a floating point number
        - 3 Informational, an integer
        - 4 Informational_Duration, a floating point number
        - 5 ProductRelated, an integer
        - 6 ProductRelated_Duration, a floating point number
        - 7 BounceRates, a floating point number
        - 8 ExitRates, a floating point number
        - 9 PageValues, a floating point number
        - 10 SpecialDay, a floating point number
        - 11 Month, an index from 0 (January) to 11 (December)
        - 12 cOperatingSystems, an integer
        - 13 Browser, an integer
        - 14 Region, an integer
        - 15 TrafficType, an integer
        - 16 VisitorType, an integer 0 (not returning) or 1 (returning)
        - 17 Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidences_list = []
        lables_list = []
        num_rows_in_csv = 0
        
        # Read the csv row by row and build the list as per the spec
        for row in reader:        
            num_rows_in_csv += 1    
            evidences_list.append([
                int(row[0]),
                float(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                month_to_int(row[10]),
                int(row[11]),
                int(row[12]),
                int(row[13]),
                int(row[14]),
                1 if row[15] == "Returning_Visitor" else 0,
                1 if row[16] == "TRUE" else 0
            ])
            if row[17] == "TRUE":
                lables_list.append(1)
            elif row[17] == "FALSE":
                lables_list.append(0)

        # Make sure the evidence_list and labels_list are equal to the number of rows in the csv file

        if not validate_load_data(num_rows_in_csv, evidences_list, lables_list):
            sys.exit("Error loading CSV file")
        
    return (evidences_list, lables_list)


def month_to_int(month):
    """
    Given the month from the csv file, return the numberical equivallent as per the spec
    """
    month_dict = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,  
        "Dec": 11
    }
    return month_dict[month]


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Sensitivity
    true_positive_rate = 0.0
    actual_positives = 0
    predicted_positives = 0

    # Loop through the lables list, if it is a postive result, increment actual_positives and compare preducted list.
    # If we correctly predicted, increment predicted_positives

    for i in range(0, len(labels)):
        if labels[i] == 1:
            actual_positives += 1
            if labels[i] == predictions[i]:
                predicted_positives += 1

    # Sensitivity is the ratio of positives tha twe correctly predicted
    
    true_positive_rate = predicted_positives/actual_positives

    # Specificity
    true_negative_rate = 0.0
    actual_negatives = 0
    predicted_negatives = 0

    # Loop through the lables list, if it is a negative result, increment negative_results and compare preducted list.
    # If we correctly predicted, increment predicted_negatives

    for i in range(0, len(labels)):
        if labels[i] == 0:
            actual_negatives += 1
            if labels[i] == predictions[i]:
                predicted_negatives += 1

    # Specificity is the ratio of negatives tha twe correctly predicted

    true_negative_rate = predicted_negatives/actual_negatives

    # Return a tuple as per the spec
    
    return (true_positive_rate, true_negative_rate)


def validate_load_data(num_rows_in_csv, evidences_list, labels_list):
    """ 
    Check if the length of evidence list and label list is equal to the number of rows
    """

    # Compare the length of evidences_list to the number of rows
    
    if len(evidences_list) != num_rows_in_csv:
        return False
    
    # Compare the length of evidences_list to the number of rows
    
    if len(labels_list) != num_rows_in_csv:
        return False

    # Looks good
    
    return True


if __name__ == "__main__":
    main()
