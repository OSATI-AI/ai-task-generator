function drawGrid(sketch) {
    sketch.stroke(200); // Light grey color for grid lines
    sketch.strokeWeight(1);

    // Draw vertical grid lines
    for (let x = 0; x < sketch.width; x += 40) {
        sketch.line(x, 0, x, sketch.height);
    }

    // Draw horizontal grid lines
    for (let y = 0; y < sketch.height; y += 40) {
        sketch.line(0, y, sketch.width, y);
    }
    }

function drawAxes(sketch) {
    sketch.stroke(0); // Black color for axes
    sketch.strokeWeight(3);
    // Draw X axis
    sketch.line(0, sketch.height / 2, sketch.width, sketch.height / 2);
    // Draw Y axis
    sketch.line(sketch.width / 2, 0, sketch.width / 2, sketch.height);
}

function drawLinearFunction(sketch, slope, offspring) {
    sketch.stroke(255, 0, 0); // Red color for the function line
    sketch.strokeWeight(2);
    sketch.beginShape();
for (let x = -sketch.width / 2; x < sketch.width / 2; x++) {
    let y = slope * x + offspring * 40; // y = x + 2, scaled to grid units (40 pixels per unit)
    sketch.vertex(sketch.width / 2 + x, sketch.height / 2 - y);
}
sketch.endShape();
}

function plot_linear_function(slope, offspring, container){
    var s = function( sketch ) {
        sketch.setup = function() {
            canvas = sketch.createCanvas(400, 400);
            canvas.parent(container);
            sketch.background(255);
            drawGrid(sketch);
            drawAxes(sketch);
            drawLinearFunction(sketch, slope, offspring);
        };
      };

    new p5(s);
    console.log("Plot Linear Function!")
};

function plot_missing_number_grid(missing_number, container){
    var s = function( sketch ) {
        sketch.setup = function() {
            canvas = sketch.createCanvas(400, 400);
            canvas.parent(container);
            sketch.background(255);

            let cols = 10;
            let rows = 10;
            let cellWidth = sketch.width / cols;
            let cellHeight = sketch.height / rows;
            let currentNumber = 1;
        
            sketch.textSize(16);
            sketch.textAlign(sketch.CENTER, sketch.CENTER);
            sketch.stroke(0);
            sketch.noFill();
        
            for (let y = 0; y < rows; y++) {
            for (let x = 0; x < cols; x++) {
                let xPos = x * cellWidth;
                let yPos = y * cellHeight;
        
                if (currentNumber !== missing_number) {
                    sketch.fill(0);
                    sketch.text(currentNumber, xPos + cellWidth / 2, yPos + cellHeight / 2);
                } else {
                    sketch.fill(255); // Make the blank cell fill white so it appears blank
                }
        
                sketch.stroke(0);
                sketch.noFill();
                sketch.rect(xPos, yPos, cellWidth, cellHeight);
        
                currentNumber++;
            }
        }
    }
        
    }
    new p5(s);
}
