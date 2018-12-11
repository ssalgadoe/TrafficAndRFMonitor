

function render(data, x, y, y1, label) {
    console.log('just render');

   // var x = "dummy";
   // var y = "rssi"
    //var y1 = "rssi"
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
      //data[i]['usage_rx'] = usage['rx'][i];
      //data[i]['usage_tx'] = usage['tx'][i];
    }

    //console.log(data)
    xScale.domain(d3.extent(data, function (d) {return d[x];}));
    ys1 = d3.extent(data, function (d) {return +d[y];});

    ys2 = d3.extent(data, function (d) {return +d[y1];});
    //console.log("ys1", ys1);
    //console.log("ys2", ys2);
    bigy = ys1;
    if (ys2[1] > ys1[1]) {
        bigy = ys2;
    }

    //console.log("big y ",  bigy);
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
      .text(label);


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


  function render_circles(data, label) {
    console.log('render circles');
    //console.log(data)
    var x = "clon_id";
    var y = "clat_id"
    var r = "rssi"
    var window_h = 600;
    var window_w = 800;

    var margin = {left:60, top:30, right:100, bottom:150};

    var frame_h = window_h - margin.top - margin.bottom;
    var frame_w = window_w - margin.left - margin.right;

    var xScale = d3.scaleLinear().range([0,frame_w]);
    var yScale = d3.scaleLinear().range([frame_h,0]);


    //console.log(data)
    //xScale.domain(d3.extent(data, function (d) {return d[x];}));

    x_scale = d3.extent(data, function (d) {return +d[x];});
    y_scale = d3.extent(data, function (d) {return +d[y];});

    if (x_scale[0] > data[0].aplon_id) {
        x_scale[0] = +data[0].aplon_id;
    }
    if (x_scale[1] < data[0].aplon_id) {
        x_scale[1] = +data[0].aplon_id;
    }
    if (y_scale[0] > data[0].aplat_id) {
        y_scale[0] = +data[0].aplat_id;
    }
    if (y_scale[1] < data[0].aplat_id) {
        y_scale[1] = +data[0].aplat_id;
    }

    r_scale = d3.extent(data, function (d) {return +d[r];});
    //console.log('rssi->scale', r_scale, data.length )
    //console.log('x->scale', x_scale )
    //console.log('y->scale', y_scale )

var colors = d3.scaleLinear()
    .domain(r_scale)
    .range(['#c12d0d','#3eed2b']);

    xScale.domain(x_scale);
    yScale.domain(y_scale);
    //rScale.domain(r_scale);


    var svg = d3.select("body").append("svg")
        .attr("width",window_w)
        .attr("height",window_h);
    //    .attr("transform","translate("+ margin.left + "," + margin.top + ")");

    var g_main = svg.append("g").attr("transform","translate("+ margin.left + "," + margin.top + ")");

    var clients = g_main.selectAll("g").data(data)
                .enter()
                .append("g")
                .attr("class", "clients")
                .attr("transform", function(d) {
                           return "translate(" + xScale(d.clon_id) + "," + yScale(d.clat_id) + ")";
                })
                .on('mouseover',function() {
                              d3.select(this).raise()
                              .append("text")
                              .attr("class","custname")
                              .text(d=>d.custname + " : " +d.rssi)
                })
                .on('mouseout',function() {
                        d3.selectAll(".custname").remove()
                })
                clients
                .append("circle")
                    .attr("fill", d=>colors(d.rssi))
                    .attr("r", d=> -d.rssi/4)
                    .attr('stroke','#595a49')
                    .attr('stroke-width',0)
                    .on('mouseover',function() {
                            d3.select(this)
                          	  .transition()
                          	  .duration(1000)
                          	  .attr('stroke-width',5)
                          })
                    .on('mouseout',function () {
                            d3.select(this)
                              .transition()
                              .duration(1000)
                              .attr('stroke-width',0)
                        })

                     .on("click", function(d) {
                          // window.open('reg_name/' + d.custname + '/')
                          location.href = 'reg_name/' + d.custname + '/'

                     })

    g_main.append("g")
        .attr("class","ap")
         .attr("transform", function(d) {
                  return "translate(" + xScale(data[0].aplon_id) + "," + yScale(data[0].aplat_id) + ")";
          })
          .on('mouseover',function() {
                d3.select(this).lower()
                .append("text")
                .attr("class","ap_text")
                .text(data[0].ap_name)
                })
          .on('mouseout',function() {
                        d3.selectAll(".ap_text").remove()
                })


          .append("circle")
            .attr("fill","#9da060")
            .attr('stroke','#595a49')
            .attr('stroke-width',2)
            .attr("r", 35)
            .on('mouseover',function() {
                    d3.select(this)
                 	  .transition()
                   	  .duration(1000)
                   	  .attr('stroke-width',5)
            })
            .on('mouseout',function () {
                    d3.select(this)
                      .transition()
                      .duration(1000)
                      .attr('stroke-width',2)
            })


 }






