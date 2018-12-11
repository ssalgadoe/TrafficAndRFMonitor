function render_towers(data, label) {
    console.log('render towers pls (5)');
    //console.log(data)
    var x = "lon_id";
    var y = "lat_id"
    var r = "size"
    var window_h = 600;
    var window_w = 800;

    var margin = {left:60, top:60, right:100, bottom:150};

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
   // console.log('size->scale', r_scale, data.length )
   // console.log('x->scale', x_scale )
   // console.log('y->scale', y_scale )

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

    var aps = g_main.selectAll("g").data(data)
                .enter()
                .append("g")
                .attr("class", "clients")
                .attr("transform", function(d) {
                           return "translate(" + xScale(d.lon_id) + "," + yScale(d.lat_id) + ")";
                })
                .on('mouseover',function() {
                              d3.select(this).raise()
                              .append("text")
                              .attr("class","custname")
                              .text(d=>d.name + " : " +d.size)
                })
                .on('mouseout',function() {
                        d3.selectAll(".custname").remove()
                })
                aps
                .append("circle")
                    .attr("fill", d=>colors(d.size))
                    .attr("r", d=> .5*d.size)
                    .attr('stroke','#595a49')
                    .attr('stroke-dasharray',"1,1")
                    .attr('stroke-width',5)
                    .on('mouseover',function() {
                            d3.select(this)
                          	  .transition()
                          	  .duration(1000)
                          	  .attr('stroke-width',10)
                          })
                    .on('mouseout',function () {
                            d3.select(this)
                              .transition()
                              .duration(1000)
                              .attr('stroke-width',5)
                        })

                     .on("click", function(d) {
                          // window.open('reg_name/' + d.custname + '/')
                          location.href =  '/registrations/aps/' + d.loc_id + '/'

                     })




 }
