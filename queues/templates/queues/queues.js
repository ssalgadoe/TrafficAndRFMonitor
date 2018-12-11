
function render(data) {
    console.log('help');

    var x = "dummy";
    var y = "usage_rx"
    var y1 = "usage_tx"
    var window_h = 400;
    var window_w = 400;

    var margin = {left:60, top:30, right:30, bottom:150};

    var frame_h = window_h - margin.top - margin.bottom;
    var frame_w = window_w - margin.left - margin.right;

    var xScale = d3.scaleLinear().range([0,frame_w]);
    var yScale = d3.scaleLinear().range([frame_h,0]);

    //var data = {{queue_data|safe}}
    //var Ax = Array.from(Array(data.length).keys());

    for (var i = 0; i < data.length; i++) {
      data[i].dummy = i;
      data[i]['usage_rx'] = usage['rx'][i];
      data[i]['usage_tx'] = usage['tx'][i];
    }

    console.log(data)
    xScale.domain(d3.extent(data, function (d) {return d[x];}));
    ys1 = d3.extent(data, function (d) {return +d[y];});
    ys2 = d3.extent(data, function (d) {return +d[y1];});
    bigy = ys1;
    if (ys2[1] > ys1[1]) {
        bigy = ys2;
    }
    console.log(ys1,ys2, bigy);
    yScale.domain(bigy);


    var xAxis = d3.axisBottom()
        .tickFormat("")
        .scale(xScale);
    var yAxis = d3.axisLeft()
         .scale(yScale);



    var svg = d3.select("body").append("svg").attr("width",window_w).attr("height",window_h);
    var g = svg.append("g").attr("transform","translate("+ margin.left + "," + margin.top + ")");

    xAxisG = g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + frame_h + ")")
        .call(xAxis)
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)");

    yAxisG = g.append("g")
        .attr("class", "y axis")
        .call(yAxis);


  g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0-margin.left)
      .attr("x",0-(frame_h/2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Average Usage (Kbps)");


  g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0)
      .attr("x",0-frame_h)
      .attr("dy", "1em")
      .style("text-anchor", "end")
      .text(d_from);

  g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", frame_w)
      .attr("x",0-frame_h)
      .attr("dy", "1em")
      .style("text-anchor", "end")
      .text(d_to);


    var path  = g.append("path");
        path.attr("class", "blue")

    var circles = g.selectAll("circle").data(data);

    var line = d3.line()
            .x(function(d){return xScale(d[x])})
            .y(function(d){return yScale(d[y])})
            .curve(d3.curveLinear);

    path.attr("d", line(data));

    var path1  = g.append("path");
        path1.attr("class", "red")

    var circles = g.selectAll("circle").data(data);

    var line = d3.line()
            .x(function(d){return xScale(d[x])})
            .y(function(d){return yScale(d[y1])})
            .curve(d3.curveLinear);

    path1.attr("d", line(data));


}