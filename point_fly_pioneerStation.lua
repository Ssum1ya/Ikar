-- Данный скрипт реализует полет по заданным точкам в системе позиционирования

-- Упрощение вызова функции распаковки таблиц из модуля table
local unpack = table.unpack


-- Таблица точек полетного задания в формате {x,y,z}
local points = {
        {0, 0, 0.7},
        {0, 1, 0.7},
        {0.5, 1, 0.7},
        {0.5, 0, 0.7}
}
-- Счетчик точек
local curr_point = 1

-- Функция, изменяющая цвет светодиодов и выполняющая полет к следующей точке
local function nextPoint()
    -- Полет к текущей точке, если её номер не больше количества заданных точек
    if(curr_point <= #points) then
        Timer.callLater(1, function()
            -- Команда полета к точке в системе позиционирования
            ap.goToLocalPoint(unpack(points[curr_point]))
            -- Инкрементация переменной текущей точки
            curr_point = curr_point + 1
        end)
    -- Посадка, если номер текущей точки больше количества заданных точек
    else
        Timer.callLater(1, function()
            -- Команда на посадку
            ap.push(Ev.MCE_LANDING)
        end)
    end
end

-- Функция обработки событий, автоматически вызывается автопилотом
function callback(event)
    -- Когда коптер поднялся на высоту взлета Flight_com_takeoffAlt, переходим к полету по точкам
    if(event == Ev.TAKEOFF_COMPLETE) then
        nextPoint()
    end
    -- Когда коптер достиг текущей точки, переходим к следующей
    if(event == Ev.POINT_REACHED) then
        nextPoint()
    end
end



-- Предстартовая подготовка
ap.push(Ev.MCE_PREFLIGHT)
-- Таймер, через 2 секунды вызывающий функцию взлета
Timer.callLater(2, function() ap.push(Ev.MCE_TAKEOFF) end)

