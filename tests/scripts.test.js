describe("Convert Arrival Time To Time in Minutes", () => {

    it("Returns arrival time in minutes after subtracting the predicted time from the arrival time.", () => {
        const arrivalTime = new Date("2021-01-08T00:34:38");
        const predictedTime = new Date("2021-01-08T00:28:38");

        expect(convertToMinutes(arrivalTime, predictedTime)).toEqual(6);
    })
})