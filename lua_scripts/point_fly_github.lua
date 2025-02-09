-- ассоциируем функцию распаковки таблиц из модуля table для упрощения
local unpack = table.unpack

-- переменная текущего состояния
local curr_state = "PREPARE_FLIGHT"
        

local points = {
        {0, 0, 0.7},
        {0.25, 0.77, 0.7},
        {0.5, 0, 0.7},
        {-0.15, 0.48, 0.7},
        {0.65, 0.48, 0.7}
}


-- таблица функций, вызываемых в зависимости от состояния
action = {
    ["PREPARE_FLIGHT"] = function()
        Timer.callLater(2, function () ap.push(Ev.MCE_PREFLIGHT) end) -- через 2 секунды отправляем команду автопилоту на запуск моторов
        Timer.callLater(6, function ()
            ap.push(Ev.MCE_TAKEOFF) -- еще через 2 секунды (суммарно через 6 секунд) отправляем команду автопилоту на взлет
            curr_state = "FLIGHT_TO_FIRST_POINT" -- переход в следующее состояние
        end)
    end,
    ["FLIGHT_TO_FIRST_POINT"] = function ()
        Timer.callLater(2, function ()
            ap.goToLocalPoint(unpack(points[1])) -- отправка команды автопилоту на полет к точке из списка points под номером 1
            curr_state = "FLIGHT_TO_SECOND_POINT" -- переход в следующее состояние
        end)
    end,
    ["FLIGHT_TO_SECOND_POINT"] = function ()
        Timer.callLater(2, function ()
            ap.goToLocalPoint(unpack(points[2])) -- отправка команды автопилоту на полет к точке из списка points под номером 2
            curr_state = "FLIGHT_TO_THIRD_POINT" -- переход в следующее состояние
        end)
    end,
    ["FLIGHT_TO_THIRD_POINT"] = function ()
        Timer.callLater(2, function ()
            ap.goToLocalPoint(unpack(points[3])) -- отправка команды автопилоту на полет к точке из списка points под номером 3
            curr_state = "FLIGHT_TO_FORTH_POINT" -- переход в следующее состояние
        end)
    end,
    ["FLIGHT_TO_FORTH_POINT"] = function ()
        Timer.callLater(2, function ()
            ap.goToLocalPoint(unpack(points[4])) -- отправка команды автопилоту на полет к точке из списка points под номером 4
            curr_state = "FLIGHT_TO_FIFTH_POINT" -- переход в следующее состояние
        end)
    end,
    ["FLIGHT_TO_FIFTH_POINT"] = function ()
        Timer.callLater(2, function ()
            ap.goToLocalPoint(unpack(points[5])) -- отправка команды автопилоту на полет к точке из списка points под номером 5
            curr_state = "PIONEER_LANDING" -- переход в следующее состояние
        end)
    end,
    ["PIONEER_LANDING"] = function ()
        Timer.callLater(2, function ()
            ap.push(Ev.MCE_LANDING) -- отправка команды автопилоту на посадку
        end)
    end
}

-- функция обработки событий, автоматически вызывается автопилотом
function callback(event)
    -- если достигнута необходимая высота, то выполняем функцию из таблицы, соответствующую текущему состоянию
    if (event == Ev.TAKEOFF_COMPLETE) then
        action[curr_state]()
    end

    -- если пионер достигнул точки, то выполняем функцию из таблицы, соответствующую текущему состоянию
    if (event == Ev.POINT_REACHED) then
        action[curr_state]()
    end
end


-- запускаем одноразовый таймер на 2 секунды, а когда он закончится, выполняем первую функцию из таблицы (подготовка к полету)
Timer.callLater(2, function () action[curr_state]() end)
